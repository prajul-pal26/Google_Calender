import streamlit as st
import requests
import json
import pandas as pd
from datetime import datetime, timedelta
import plotly.graph_objects as go
import plotly.express as px
from typing import Dict, List
import time
import os
import json

# Configuration
PAGE_CONFIG = {
    "page_title": "Google Calendar Pause/Resume Manager",
    "page_icon": "📅",
    "layout": "wide",
    "initial_sidebar_state": "expanded"
}

st.set_page_config(**PAGE_CONFIG)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .status-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        margin: 1rem 0;
    }
    .success-message {
        background-color: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 5px;
        border: 1px solid #c3e6cb;
    }
    .error-message {
        background-color: #f8d7da;
        color: #721c24;
        padding: 1rem;
        border-radius: 5px;
        border: 1px solid #f5c6cb;
    }
    .warning-message {
        background-color: #fff3cd;
        color: #856404;
        padding: 1rem;
        border-radius: 5px;
        border: 1px solid #ffeaa7;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        text-align: center;
        color: white;
        border: 2px solid rgba(255,255,255,0.1);
    }
    .metric-card h3 {
        color: white !important;
        font-size: 2.5rem !important;
        font-weight: bold !important;
        margin: 0 !important;
    }
    .metric-card p {
        color: rgba(255,255,255,0.9) !important;
        font-size: 1rem !important;
        margin: 0.5rem 0 0 0 !important;
    }
    .pause-button {
        background: linear-gradient(45deg, #ff6b6b, #ee5a24);
        color: white;
        border: none;
        padding: 1rem 2rem;
        border-radius: 10px;
        font-size: 1.2rem;
        font-weight: bold;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    .resume-button {
        background: linear-gradient(45deg, #4ecdc4, #44a08d);
        color: white;
        border: none;
        padding: 1rem 2rem;
        border-radius: 10px;
        font-size: 1.2rem;
        font-weight: bold;
        cursor: pointer;
        transition: all 0.3s ease;
    }
</style>
""", unsafe_allow_html=True)

# Google Calendar API integration
import os
from datetime import datetime, timedelta
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from typing import Optional, Dict

# Global variables for Google Calendar
SCOPES = ["https://www.googleapis.com/auth/calendar"]
DEFAULT_TIMEZONE = "Asia/Kolkata"

# In-memory storage for paused events
paused_events = {}
last_paused_event_id = None
configured_calendar_id = None

def get_service():
    """Get Google Calendar service instance"""
    try:
        # Use public configuration file for service account info
        if os.path.exists("service_account.json"):
            creds = Credentials.from_service_account_file("service_account.json", scopes=SCOPES)
        else:
            st.error("❌ Service account file not found. Please upload service_account.json")
            return None
            
        service = build("calendar", "v3", credentials=creds)
        return service
    except Exception as e:
        st.error(f"Failed to connect to Google Calendar: {str(e)}")
        return None

def get_current_ongoing_event():
    """Get the current/ongoing event at this moment"""
    global configured_calendar_id
    
    if not configured_calendar_id:
        return None
    
    service = get_service()
    if not service:
        return None
    
    try:
        now = datetime.utcnow().isoformat() + 'Z'
        
        events_result = service.events().list(
            calendarId=configured_calendar_id,
            timeMin=now,
            maxResults=10,
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        
        events = events_result.get('items', [])
        current_time = datetime.now(datetime.utcnow().astimezone().tzinfo)
        
        for event in events:
            if event.get('summary', '').startswith('[COMPLETED]'):
                continue
                
            start_time = datetime.fromisoformat(event['start']['dateTime'].replace('Z', '+00:00'))
            end_time = datetime.fromisoformat(event['end']['dateTime'].replace('Z', '+00:00'))
            
            if start_time <= current_time <= end_time:
                return event
        
        return None
    except Exception as e:
        st.error(f"Error getting current event: {str(e)}")
        return None

def find_available_slot(start_time: datetime, duration: timedelta, service):
    """Find the next available slot for the given duration"""
    global configured_calendar_id
    
    try:
        time_min = start_time.isoformat()
        time_max = (start_time + timedelta(days=7)).isoformat()
        
        events_result = service.events().list(
            calendarId=configured_calendar_id,
            timeMin=time_min,
            timeMax=time_max,
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        
        events = events_result.get('items', [])
        sorted_events = sorted(events, key=lambda x: x['start']['dateTime'])
        
        current_time = start_time
        end_time = start_time + duration
        
        for event in sorted_events:
            event_start = datetime.fromisoformat(event['start']['dateTime'].replace('Z', '+00:00'))
            event_end = datetime.fromisoformat(event['end']['dateTime'].replace('Z', '+00:00'))
            
            if current_time + duration <= event_start:
                return current_time, end_time
            
            if event_end > current_time:
                current_time = event_end
                end_time = current_time + duration
        
        return current_time, end_time
    except Exception as e:
        st.error(f"Error finding available slot: {str(e)}")
        return start_time, start_time + duration

def create_event_in_past(event_name: str, start_time: datetime, end_time: datetime):
    """Create an event in the past to record the completed portion"""
    global configured_calendar_id
    
    service = get_service()
    if not service:
        return None
    
    try:
        event_data = {
            "summary": f"[COMPLETED] {event_name}",
            "start": {"dateTime": start_time.isoformat(), "timeZone": "UTC"},
            "end": {"dateTime": end_time.isoformat(), "timeZone": "UTC"},
        }
        
        created_event = service.events().insert(
            calendarId=configured_calendar_id,
            body=event_data
        ).execute()
        
        return created_event
    except Exception as e:
        st.error(f"Error creating completed event: {str(e)}")
        return None

def auto_reschedule_abandoned_events():
    """Reschedule events that have been paused for too long without resume"""
    global paused_events, configured_calendar_id
    
    if not configured_calendar_id or not paused_events:
        return
    
    service = get_service()
    if not service:
        return
    
    current_time = datetime.now(datetime.utcnow().astimezone().tzinfo)
    events_to_reschedule = []
    
    for event_id, pause_info in list(paused_events.items()):
        original_end_time = pause_info["original_end_time"]
        pause_time = pause_info["pause_time"]
        
        time_since_original_end = current_time - original_end_time
        time_since_pause = current_time - pause_time
        
        should_reschedule = (
            (time_since_original_end > timedelta(minutes=30)) or
            (time_since_pause > timedelta(hours=2))
        )
        
        if should_reschedule:
            events_to_reschedule.append((event_id, pause_info, time_since_original_end, time_since_pause))
    
    for event_id, pause_info, time_since_original_end, time_since_pause in events_to_reschedule:
        try:
            available_start, available_end = find_available_slot(
                current_time,
                pause_info["remaining_duration"],
                service
            )
            
            if time_since_original_end > timedelta(minutes=30):
                summary = f"[MISSED] {pause_info['event_name']}"
            else:
                summary = f"[RESCHEDULED] {pause_info['event_name']}"
            
            event_data = {
                "summary": summary,
                "start": {"dateTime": available_start.isoformat(), "timeZone": "UTC"},
                "end": {"dateTime": available_end.isoformat(), "timeZone": "UTC"},
                "description": f"Auto-rescheduled after {time_since_pause.total_seconds()/3600:.1f} hours pause. Original end time was {pause_info['original_end_time'].strftime('%Y-%m-%d %H:%M')}"
            }
            
            created_event = service.events().insert(
                calendarId=configured_calendar_id,
                body=event_data
            ).execute()
            
            del paused_events[event_id]
            
            global last_paused_event_id
            if last_paused_event_id == event_id:
                last_paused_event_id = None
            
            st.success(f"Auto-rescheduled event: {pause_info['event_name']} -> {summary}")
            
        except Exception as e:
            st.error(f"Failed to auto-reschedule event {event_id}: {str(e)}")

def pause_current_event():
    """Pause the current ongoing event"""
    global configured_calendar_id, paused_events, last_paused_event_id
    
    if not configured_calendar_id:
        return {"error": "Calendar not configured"}
    
    try:
        auto_reschedule_abandoned_events()
        
        current_event = get_current_ongoing_event()
        
        if not current_event:
            return {"error": "No ongoing event found at this time"}
        
        service = get_service()
        if not service:
            return {"error": "Failed to connect to Google Calendar"}
        
        event_name = current_event.get('summary', 'Unknown Event')
        
        start_time = datetime.fromisoformat(current_event['start']['dateTime'].replace('Z', '+00:00'))
        original_end_time = datetime.fromisoformat(current_event['end']['dateTime'].replace('Z', '+00:00'))
        current_time = datetime.now(start_time.tzinfo)
        
        remaining_duration = original_end_time - current_time
        
        completed_event = create_event_in_past(
            event_name,
            start_time,
            current_time
        )
        
        if not completed_event:
            return {"error": "Failed to create completed event"}
        
        service.events().delete(
            calendarId=configured_calendar_id,
            eventId=current_event['id']
        ).execute()
        
        pause_info = {
            "event_name": event_name,
            "original_event": current_event,
            "pause_time": current_time,
            "remaining_duration": remaining_duration,
            "original_end_time": original_end_time
        }
        
        paused_events[current_event['id']] = pause_info
        last_paused_event_id = current_event['id']
        
        return {
            "message": f"Event '{event_name}' paused successfully",
            "event_name": event_name,
            "event_id": current_event['id'],
            "paused_at": current_time.isoformat(),
            "remaining_duration": str(remaining_duration),
            "completed_event_id": completed_event.get("id"),
            "original_end_time": original_end_time.isoformat()
        }
        
    except Exception as e:
        return {"error": f"Failed to pause event: {str(e)}"}

def resume_last_event():
    """Resume the most recently paused event"""
    global configured_calendar_id, paused_events, last_paused_event_id
    
    if not configured_calendar_id:
        return {"error": "Calendar not configured"}
    
    try:
        if not last_paused_event_id or last_paused_event_id not in paused_events:
            return {"error": "No paused event found to resume"}
        
        pause_info = paused_events[last_paused_event_id]
        current_time = datetime.now(pause_info["pause_time"].tzinfo)
        
        pause_duration = current_time - pause_info["pause_time"]
        
        service = get_service()
        if not service:
            return {"error": "Failed to connect to Google Calendar"}
        
        proposed_start_time = current_time
        proposed_end_time = proposed_start_time + pause_info["remaining_duration"]
        
        available_start, available_end = find_available_slot(
            proposed_start_time,
            pause_info["remaining_duration"],
            service
        )
        
        event_data = {
            "summary": pause_info["event_name"],
            "start": {"dateTime": available_start.isoformat(), "timeZone": "UTC"},
            "end": {"dateTime": available_end.isoformat(), "timeZone": "UTC"},
        }
        
        created_event = service.events().insert(
            calendarId=configured_calendar_id,
            body=event_data
        ).execute()
        
        del paused_events[last_paused_event_id]
        last_paused_event_id = None
        
        return {
            "message": f"Event '{pause_info['event_name']}' resumed successfully",
            "event_name": pause_info["event_name"],
            "resumed_at": available_start.isoformat(),
            "ends_at": available_end.isoformat(),
            "duration": str(pause_info["remaining_duration"]),
            "pause_duration": str(pause_duration),
            "event_id": created_event.get("id"),
            "event_link": created_event.get("htmlLink"),
            "rescheduled": available_start != proposed_start_time
        }
        
    except Exception as e:
        return {"error": f"Failed to resume event: {str(e)}"}

def get_all_events():
    """Get all events from calendar"""
    global configured_calendar_id
    
    if not configured_calendar_id:
        return {"error": "Calendar not configured"}
    
    service = get_service()
    if not service:
        return {"error": "Failed to connect to Google Calendar"}
    
    try:
        events_result = service.events().list(
            calendarId=configured_calendar_id,
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        
        events = events_result.get('items', [])
        event_list = []
        
        for event in events:
            event_info = {
                "event_id": event.get('id'),
                "event_name": event.get('summary', 'No Title'),
                "start_time": event.get('start', {}).get('dateTime', event.get('start', {}).get('date', 'N/A')),
                "end_time": event.get('end', {}).get('dateTime', event.get('end', {}).get('date', 'N/A')),
                "status": event.get('status', 'confirmed')
            }
            event_list.append(event_info)
        
        return {
            "message": f"Found {len(event_list)} events in calendar",
            "total_events": len(event_list),
            "events": event_list
        }
        
    except Exception as e:
        return {"error": f"Failed to retrieve events: {str(e)}"}

def create_new_event(event_name: str, start_datetime: str, end_datetime: str, timezone: str = DEFAULT_TIMEZONE):
    """Create a new event"""
    global configured_calendar_id
    
    if not configured_calendar_id:
        return {"error": "Calendar not configured"}
    
    service = get_service()
    if not service:
        return {"error": "Failed to connect to Google Calendar"}
    
    try:
        event_data = {
            "summary": event_name,
            "start": {"dateTime": start_datetime, "timeZone": timezone},
            "end": {"dateTime": end_datetime, "timeZone": timezone},
        }
        
        created_event = service.events().insert(
            calendarId=configured_calendar_id,
            body=event_data
        ).execute()
        
        return {
            "message": "Event created successfully",
            "event_id": created_event.get("id"),
            "event_link": created_event.get("htmlLink"),
            "event_name": event_name,
            "start_time": start_datetime,
            "end_time": end_datetime,
            "timezone_used": timezone
        }
        
    except Exception as e:
        return {"error": f"Failed to create event: {str(e)}"}

def delete_event_by_name(event_name: str):
    """Delete events by name"""
    global configured_calendar_id
    
    if not configured_calendar_id:
        return {"error": "Calendar not configured"}
    
    service = get_service()
    if not service:
        return {"error": "Failed to connect to Google Calendar"}
    
    try:
        events_result = service.events().list(
            calendarId=configured_calendar_id,
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        
        events = events_result.get('items', [])
        deleted_events = []
        
        for event in events:
            if event.get('summary') == event_name:
                service.events().delete(
                    calendarId=configured_calendar_id,
                    eventId=event['id']
                ).execute()
                deleted_events.append({
                    "event_id": event['id'],
                    "event_name": event.get('summary'),
                    "start_time": event.get('start', {}).get('dateTime', 'N/A'),
                    "end_time": event.get('end', {}).get('dateTime', 'N/A')
                })
        
        if not deleted_events:
            return {
                "message": f"No events found with name '{event_name}'",
                "deleted_count": 0
            }
        
        return {
            "message": f"Successfully deleted {len(deleted_events)} event(s) with name '{event_name}'",
            "deleted_count": len(deleted_events),
            "deleted_events": deleted_events
        }
        
    except Exception as e:
        return {"error": f"Failed to delete event: {str(e)}"}

def configure_calendar(gmail: str):
    """Configure calendar"""
    global configured_calendar_id
    
    try:
        service = get_service()
        if not service:
            return {"error": "Failed to connect to Google Calendar"}
        
        calendar = service.calendars().get(calendarId=gmail).execute()
        configured_calendar_id = gmail
        
        return {"message": f"Calendar configured successfully for {gmail}", "calendar_name": calendar.get("summary")}
    except Exception as e:
        return {"error": f"Failed to access calendar {gmail}: {str(e)}"}

# Initialize session state
if 'configured' not in st.session_state:
    st.session_state.configured = False
if 'calendar_id' not in st.session_state:
    st.session_state.calendar_id = ""
if 'last_action' not in st.session_state:
    st.session_state.last_action = ""
if 'events_data' not in st.session_state:
    st.session_state.events_data = []

def show_dashboard():
    """Show main dashboard"""
    st.markdown('<h1 class="main-header">📅 Google Calendar Pause/Resume Manager</h1>', unsafe_allow_html=True)
    
    # Quick Actions Section
    st.markdown("## ⚡ Quick Actions")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("⏸️ Pause Current Event", type="secondary", use_container_width=True):
            with st.spinner("Pausing current event..."):
                result = pause_current_event()
                if "error" not in result:
                    st.session_state.last_action = f"Paused: {result.get('event_name', 'Unknown event')}"
                    st.success(f"✅ {result.get('message', 'Event paused successfully!')}")
                    st.rerun()
                else:
                    st.error(f"❌ {result['error']}")
    
    with col2:
        if st.button("▶️ Resume Last Event", type="secondary", use_container_width=True):
            with st.spinner("Resuming event..."):
                result = resume_last_event()
                if "error" not in result:
                    st.session_state.last_action = f"Resumed: {result.get('event_name', 'Unknown event')}"
                    st.success(f"✅ {result.get('message', 'Event resumed successfully!')}")
                    st.rerun()
                else:
                    st.error(f"❌ {result['error']}")
    
    with col3:
        if st.button("🔄 Refresh All", type="secondary", use_container_width=True):
            st.rerun()
    
    # Status Cards
    st.markdown("## 📊 Current Status")
    
    # Get current status
    paused_count = len(paused_events)
    events_result = get_all_events()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_events = len(events_result.get('events', [])) if "error" not in events_result else 0
        st.markdown(f"""
        <div class="metric-card">
            <h3>{total_events}</h3>
            <p>Total Events</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <h3>{paused_count}</h3>
            <p>Paused Events</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        completed_events = len([e for e in events_result.get('events', []) if '[COMPLETED]' in e.get('event_name', '')]) if "error" not in events_result else 0
        st.markdown(f"""
        <div class="metric-card">
            <h3>{completed_events}</h3>
            <p>Completed Events</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        calendar_display = st.session_state.calendar_id[:20] + "..." if len(st.session_state.calendar_id) > 20 else st.session_state.calendar_id
        st.markdown(f"""
        <div class="metric-card">
            <h3 style="font-size: 1.2rem !important;">{calendar_display}</h3>
            <p>Calendar ID</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Last Action
    if st.session_state.last_action:
        st.markdown(f"""
        <div class="success-message">
            <strong>Last Action:</strong> {st.session_state.last_action}
        </div>
        """, unsafe_allow_html=True)
    
    # Paused Events Section
    if paused_events:
        st.markdown("## ⏸️ Currently Paused Events")
        
        for event_id, pause_info in paused_events.items():
            with st.expander(f"🔄 {pause_info['event_name']} (Paused {pause_info['paused_at'][:16]})"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write(f"**Event ID:** {event_id}")
                    st.write(f"**Paused At:** {pause_info['paused_at']}")
                    st.write(f"**Remaining Duration:** {pause_info['remaining_duration']}")
                
                with col2:
                    st.write(f"**Original End Time:** {pause_info['original_end_time'][:16]}")
                    st.write(f"**Is Last Paused:** {'✅ Yes' if event_id == last_paused_event_id else '❌ No'}")
                    
                    if event_id == last_paused_event_id:
                        if st.button(f"Resume {pause_info['event_name']}", key=f"resume_{event_id}"):
                            with st.spinner("Resuming event..."):
                                result = resume_last_event()
                                if "error" not in result:
                                    st.session_state.last_action = f"Resumed: {result.get('event_name', 'Unknown event')}"
                                    st.success(f"✅ {result.get('message', 'Event resumed successfully!')}")
                                    st.rerun()
                                else:
                                    st.error(f"❌ {result['error']}")

def show_event_management():
    """Show event management interface"""
    st.markdown("## 📝 Event Management")
    
    tab1, tab2, tab3 = st.tabs(["Create Event", "View Events", "Delete Event"])
    
    with tab1:
        st.markdown("### ➕ Create New Event")
        
        with st.form("create_event_form"):
            event_name = st.text_input("Event Name", placeholder="Study Session, Meeting, etc.")
            
            col1, col2 = st.columns(2)
            with col1:
                start_date = st.date_input("Start Date")
                start_time = st.time_input("Start Time")
            
            with col2:
                end_date = st.date_input("End Date")
                end_time = st.time_input("End Time")
            
            timezone = st.selectbox("Timezone", [
                "Asia/Kolkata", "UTC", "America/New_York", 
                "Europe/London", "Asia/Tokyo"
            ])
            
            submit_create = st.form_submit_button("Create Event", type="primary")
            
            if submit_create and event_name:
                start_datetime = datetime.combine(start_date, start_time).isoformat()
                end_datetime = datetime.combine(end_date, end_time).isoformat()
                
                with st.spinner("Creating event..."):
                    result = create_new_event(event_name, start_datetime, end_datetime, timezone)
                    if "error" not in result:
                        st.success(f"✅ {result.get('message', 'Event created successfully!')}")
                        st.info(f"🔗 [Event Link]({result.get('event_link', '#')})")
                    else:
                        st.error(f"❌ {result['error']}")
    
    with tab2:
        st.markdown("### 📋 All Events")
        
        if st.button("Refresh Events", key="refresh_events"):
            with st.spinner("Fetching events..."):
                result = get_all_events()
                if "error" not in result:
                    st.session_state.events_data = result.get('events', [])
                else:
                    st.error(f"❌ {result['error']}")
        
        if st.session_state.events_data:
            df = pd.DataFrame(st.session_state.events_data)
            
            if 'start_time' in df.columns:
                df['start_time'] = pd.to_datetime(df['start_time']).dt.strftime('%Y-%m-%d %H:%M')
            if 'end_time' in df.columns:
                df['end_time'] = pd.to_datetime(df['end_time']).dt.strftime('%Y-%m-%d %H:%M')
            
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No events found. Click 'Refresh Events' to load events.")
    
    with tab3:
        st.markdown("### 🗑️ Delete Event")
        
        with st.form("delete_event_form"):
            event_name_to_delete = st.text_input(
                "Event Name to Delete",
                placeholder="Enter exact event name",
                help="This will delete ALL events with this name"
            )
            
            submit_delete = st.form_submit_button("Delete Event", type="primary")
            
            if submit_delete and event_name_to_delete:
                if st.checkbox(f"⚠️ Confirm deletion of '{event_name_to_delete}'"):
                    with st.spinner("Deleting event..."):
                        result = delete_event_by_name(event_name_to_delete)
                        if "error" not in result:
                            deleted_count = result.get('deleted_count', 0)
                            if deleted_count > 0:
                                st.success(f"✅ {result.get('message', 'Events deleted successfully!')}")
                                for event in result.get('deleted_events', []):
                                    st.info(f"🗑️ Deleted: {event['event_name']} ({event['start_time']} - {event['end_time']})")
                            else:
                                st.warning(f"⚠️ {result.get('message', 'No events found')}")
                        else:
                            st.error(f"❌ {result['error']}")
                else:
                    st.warning("⚠️ Please confirm the deletion")

def main():
    """Main application"""
    # Sidebar
    with st.sidebar:
        st.markdown("## 🎛️ Control Panel")
        
        if st.session_state.configured:
            st.success(f"✅ Configured: {st.session_state.calendar_id}")
            
            if st.button("🔄 Reconfigure Calendar"):
                st.session_state.configured = False
                st.session_state.calendar_id = ""
                st.rerun()
        else:
            st.warning("⚠️ Calendar not configured")
        
        st.markdown("---")
        
        # Navigation
        page = st.selectbox(
            "📍 Navigate to",
            ["🏠 Dashboard", "📝 Event Management"],
            index=0
        )
        
        st.markdown("---")
        
        # Service Account Info
        st.markdown("### 🔑 Service Account")
        if os.path.exists("service_account.json"):
            st.success("✅ Service account file found")
        else:
            st.error("❌ Service account file not found")
            st.info("Upload your service_account.json file to the app directory")
        
        st.markdown("---")
        
        # Quick Stats
        st.markdown("### 📊 Quick Stats")
        st.metric("Paused Events", len(paused_events))
        
        events_result = get_all_events()
        if "error" not in events_result:
            total_events = len(events_result.get('events', []))
            st.metric("Total Events", total_events)
    
    # Main content
    if not st.session_state.configured:
        st.markdown('<h1 class="main-header">📅 Welcome to Google Calendar Manager</h1>', unsafe_allow_html=True)
        st.markdown("### Please configure your calendar to get started")
        
        with st.form("config_form"):
            calendar_id = st.text_input(
                "Enter your Gmail address",
                placeholder="example@gmail.com",
                help="This is the Gmail address associated with your Google Calendar"
            )
            
            submit_button = st.form_submit_button("Configure Calendar", type="primary")
            
            if submit_button and calendar_id:
                with st.spinner("Configuring calendar..."):
                    result = configure_calendar(calendar_id)
                    if "error" not in result:
                        st.session_state.configured = True
                        st.session_state.calendar_id = calendar_id
                        st.success(f"✅ {result.get('message', 'Calendar configured successfully!')}")
                        st.rerun()
                    else:
                        st.error(f"❌ {result['error']}")
    else:
        if page == "🏠 Dashboard":
            show_dashboard()
        elif page == "📝 Event Management":
            show_event_management()

if __name__ == "__main__":
    main()