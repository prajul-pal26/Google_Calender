import streamlit as st
import requests
import json
import pandas as pd
from datetime import datetime, timedelta
import plotly.graph_objects as go
import plotly.express as px
from typing import Dict, List
import time

# Configuration
BASE_URL = "http://localhost:8000"
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

# Initialize session state
if 'configured' not in st.session_state:
    st.session_state.configured = False
if 'calendar_id' not in st.session_state:
    st.session_state.calendar_id = ""
if 'last_action' not in st.session_state:
    st.session_state.last_action = ""
if 'events_data' not in st.session_state:
    st.session_state.events_data = []

def make_api_request(method: str, endpoint: str, data: Dict = None) -> Dict:
    """Make API request to the FastAPI server"""
    try:
        url = f"{BASE_URL}{endpoint}"
        
        if method == "GET":
            response = requests.get(url)
        elif method == "POST":
            response = requests.post(url, json=data)
        elif method == "DELETE":
            response = requests.delete(url, json=data)
        
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"API Error: {response.status_code} - {response.text}"}
    
    except requests.exceptions.ConnectionError:
        return {"error": "Connection Error: Make sure the FastAPI server is running on http://localhost:8000"}
    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}

def configure_calendar():
    """Configure the calendar"""
    st.markdown("### 📧 Calendar Configuration")
    
    with st.form("config_form"):
        calendar_id = st.text_input(
            "Enter your Gmail address",
            placeholder="example@gmail.com",
            help="This is the Gmail address associated with your Google Calendar"
        )
        
        submit_button = st.form_submit_button("Configure Calendar", type="primary")
        
        if submit_button and calendar_id:
            with st.spinner("Configuring calendar..."):
                result = make_api_request("POST", "/configure-calendar", {"gmail": calendar_id})
                
                if "error" not in result:
                    st.session_state.configured = True
                    st.session_state.calendar_id = calendar_id
                    st.success(f"✅ {result.get('message', 'Calendar configured successfully!')}")
                    st.rerun()
                else:
                    st.error(f"❌ {result['error']}")

def show_dashboard():
    """Show main dashboard"""
    # Header
    st.markdown('<h1 class="main-header">📅 Google Calendar Pause/Resume Manager</h1>', unsafe_allow_html=True)
    
    # Quick Actions Section
    st.markdown("## ⚡ Quick Actions")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("⏸️ Pause Current Event", type="secondary", use_container_width=True):
            with st.spinner("Pausing current event..."):
                result = make_api_request("POST", "/pause-event", {})
                if "error" not in result:
                    st.session_state.last_action = f"Paused: {result.get('event_name', 'Unknown event')}"
                    st.success(f"✅ {result.get('message', 'Event paused successfully!')}")
                    st.rerun()
                else:
                    st.error(f"❌ {result['error']}")
    
    with col2:
        if st.button("▶️ Resume Last Event", type="secondary", use_container_width=True):
            with st.spinner("Resuming event..."):
                result = make_api_request("POST", "/resume-event", {})
                if "error" not in result:
                    st.session_state.last_action = f"Resumed: {result.get('event_name', 'Unknown event')}"
                    st.success(f"✅ {result.get('message', 'Event resumed successfully!')}")
                    st.rerun()
                else:
                    st.error(f"❌ {result['error']}")
    
    with col3:
        if st.button("🔄 Refresh All", type="secondary", use_container_width=True):
            with st.spinner("Refreshing data..."):
                st.rerun()
    
    # Status Cards
    st.markdown("## 📊 Current Status")
    
    # Get current status
    paused_events_result = make_api_request("GET", "/paused-events")
    events_result = make_api_request("GET", "/events")
    expired_result = make_api_request("GET", "/check-expired-events")
    
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
        paused_count = len(paused_events_result.get('paused_events', [])) if "error" not in paused_events_result else 0
        st.markdown(f"""
        <div class="metric-card">
            <h3>{paused_count}</h3>
            <p>Paused Events</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        expired_count = len(expired_result.get('expired_events', [])) if "error" not in expired_result else 0
        st.markdown(f"""
        <div class="metric-card">
            <h3>{expired_count}</h3>
            <p>Expired Events</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <h3>{st.session_state.calendar_id}</h3>
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
    if "error" not in paused_events_result and paused_events_result.get('paused_events'):
        st.markdown("## ⏸️ Currently Paused Events")
        
        for event in paused_events_result['paused_events']:
            with st.expander(f"🔄 {event['event_name']} (Paused {event['paused_at'][:16]})"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write(f"**Event ID:** {event['event_id']}")
                    st.write(f"**Paused At:** {event['paused_at']}")
                    st.write(f"**Remaining Duration:** {event['remaining_duration']}")
                
                with col2:
                    st.write(f"**Original End Time:** {event['original_end_time'][:16]}")
                    st.write(f"**Is Last Paused:** {'✅ Yes' if event['is_last_paused'] else '❌ No'}")
                    
                    if event['is_last_paused']:
                        if st.button(f"Resume {event['event_name']}", key=f"resume_{event['event_id']}"):
                            with st.spinner("Resuming event..."):
                                result = make_api_request("POST", "/resume-event", {})
                                if "error" not in result:
                                    st.session_state.last_action = f"Resumed: {result.get('event_name', 'Unknown event')}"
                                    st.success(f"✅ {result.get('message', 'Event resumed successfully!')}")
                                    st.rerun()
                                else:
                                    st.error(f"❌ {result['error']}")
    
    # Expired Events Section
    if "error" not in expired_result and expired_result.get('expired_events'):
        st.markdown("## ⚠️ Expired Events (Need Rescheduling)")
        
        for event in expired_result['expired_events']:
            with st.expander(f"⏰ {event['event_name']} (Expired {event['time_since_original_end_minutes']:.1f} min ago)"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write(f"**Event ID:** {event['event_id']}")
                    st.write(f"**Paused At:** {event['paused_at'][:16]}")
                    st.write(f"**Original End Time:** {event['original_end_time'][:16]}")
                
                with col2:
                    st.write(f"**Time Since Original End:** {event['time_since_original_end_minutes']:.1f} minutes")
                    st.write(f"**Time Since Pause:** {event['time_since_pause_hours']:.1f} hours")
                    st.write(f"**Will Be Labeled:** {event['will_be_labeled']}")
                    st.write(f"**Remaining Duration:** {event['remaining_duration']}")
        
        if st.button("🔄 Force Reschedule All Expired Events", type="primary"):
            with st.spinner("Rescheduling expired events..."):
                result = make_api_request("POST", "/force-reschedule-expired", {})
                if "error" not in result:
                    st.success(f"✅ {result.get('message', 'Events rescheduled successfully!')}")
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
                # Combine date and time
                start_datetime = datetime.combine(start_date, start_time).isoformat()
                end_datetime = datetime.combine(end_date, end_time).isoformat()
                
                event_data = {
                    "event_name": event_name,
                    "start_datetime": start_datetime,
                    "end_datetime": end_datetime,
                    "timezone": timezone
                }
                
                with st.spinner("Creating event..."):
                    result = make_api_request("POST", "/create-event", event_data)
                    if "error" not in result:
                        st.success(f"✅ {result.get('message', 'Event created successfully!')}")
                        st.info(f"🔗 [Event Link]({result.get('event_link', '#')})")
                    else:
                        st.error(f"❌ {result['error']}")
    
    with tab2:
        st.markdown("### 📋 All Events")
        
        if st.button("Refresh Events", key="refresh_events"):
            with st.spinner("Fetching events..."):
                result = make_api_request("GET", "/events")
                if "error" not in result:
                    st.session_state.events_data = result.get('events', [])
                else:
                    st.error(f"❌ {result['error']}")
        
        if st.session_state.events_data:
            # Convert to DataFrame for better display
            df = pd.DataFrame(st.session_state.events_data)
            
            # Format datetime columns
            if 'start_time' in df.columns:
                df['start_time'] = pd.to_datetime(df['start_time']).dt.strftime('%Y-%m-%d %H:%M')
            if 'end_time' in df.columns:
                df['end_time'] = pd.to_datetime(df['end_time']).dt.strftime('%Y-%m-%d %H:%M')
            
            st.dataframe(df, use_container_width=True)
            
            # Event timeline visualization
            if len(df) > 0:
                st.markdown("#### 📈 Event Timeline")
                
                # Create timeline chart
                fig = px.timeline(
                    df, 
                    x_start="start_time", 
                    x_end="end_time", 
                    y="event_name",
                    title="Event Timeline",
                    color="event_name"
                )
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)
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
                        result = make_api_request("DELETE", "/delete-event", {"event_name": event_name_to_delete})
                        if "error" not in result:
                            deleted_count = result.get('deleted_count', 0)
                            if deleted_count > 0:
                                st.success(f"✅ {result.get('message', 'Events deleted successfully!')}")
                                # Show deleted events
                                for event in result.get('deleted_events', []):
                                    st.info(f"🗑️ Deleted: {event['event_name']} ({event['start_time']} - {event['end_time']})")
                            else:
                                st.warning(f"⚠️ {result.get('message', 'No events found')}")
                        else:
                            st.error(f"❌ {result['error']}")
                else:
                    st.warning("⚠️ Please confirm the deletion")

def show_analytics():
    """Show analytics and insights"""
    st.markdown("## 📈 Analytics & Insights")
    
    # Get data
    events_result = make_api_request("GET", "/events")
    paused_result = make_api_request("GET", "/paused-events")
    
    if "error" not in events_result and "error" not in paused_result:
        events = events_result.get('events', [])
        paused_events = paused_result.get('paused_events', [])
        
        # Event Statistics
        st.markdown("### 📊 Event Statistics")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            total_events = len(events)
            completed_events = len([e for e in events if '[COMPLETED]' in e.get('event_name', '')])
            st.metric("Total Events", total_events)
            st.metric("Completed Events", completed_events)
        
        with col2:
            missed_events = len([e for e in events if '[MISSED]' in e.get('event_name', '')])
            rescheduled_events = len([e for e in events if '[RESCHEDULED]' in e.get('event_name', '')])
            st.metric("Missed Events", missed_events)
            st.metric("Rescheduled Events", rescheduled_events)
        
        with col3:
            active_events = total_events - completed_events - missed_events - rescheduled_events
            st.metric("Active Events", active_events)
            st.metric("Paused Events", len(paused_events))
        
        # Event Status Distribution
        if events:
            st.markdown("### 📊 Event Status Distribution")
            
            status_counts = {
                'Active': active_events,
                'Completed': completed_events,
                'Missed': missed_events,
                'Rescheduled': rescheduled_events
            }
            
            fig = go.Figure(data=[
                go.Bar(x=list(status_counts.keys()), y=list(status_counts.values()))
            ])
            fig.update_layout(title="Event Status Distribution", xaxis_title="Status", yaxis_title="Count")
            st.plotly_chart(fig, use_container_width=True)
        
        # Paused Events Analysis
        if paused_events:
            st.markdown("### ⏸️ Paused Events Analysis")
            
            for event in paused_events:
                with st.expander(f"🔄 {event['event_name']}"):
                    # Calculate pause duration
                    paused_time = datetime.fromisoformat(event['paused_at'].replace('Z', '+00:00'))
                    current_time = datetime.now()
                    pause_duration = current_time - paused_time
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write(f"**Paused For:** {pause_duration}")
                        st.write(f"**Remaining Time:** {event['remaining_duration']}")
                    
                    with col2:
                        st.write(f"**Original End:** {event['original_end_time'][:16]}")
                        st.write(f"**Is Last Paused:** {'✅' if event['is_last_paused'] else '❌'}")
                    
                    # Progress bar for time remaining
                    remaining_parts = event['remaining_duration'].split(':')
                    if len(remaining_parts) >= 2:
                        hours = int(remaining_parts[0])
                        minutes = int(remaining_parts[1])
                        total_minutes = hours * 60 + minutes
                        
                        st.progress(0.7, f"Time remaining: {event['remaining_duration']}")
    else:
        st.error("❌ Unable to fetch analytics data")

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
            ["🏠 Dashboard", "📝 Event Management", "📈 Analytics"],
            index=0
        )
        
        st.markdown("---")
        
        # Server Status
        st.markdown("### 🖥️ Server Status")
        
        if st.button("🔍 Check Server"):
            result = make_api_request("GET", "/")
            if "error" not in result:
                st.success("✅ Server is running")
                st.info(f"Calendar: {result.get('configured_calendar', 'Not set')}")
            else:
                st.error("❌ Server is not running")
                st.info("Start server with: `python app.py`")
        
        st.markdown("---")
        
        # Quick Stats
        st.markdown("### 📊 Quick Stats")
        
        paused_result = make_api_request("GET", "/paused-events")
        if "error" not in paused_result:
            paused_count = len(paused_result.get('paused_events', []))
            st.metric("Paused Events", paused_count)
        
        expired_result = make_api_request("GET", "/check-expired-events")
        if "error" not in expired_result:
            expired_count = len(expired_result.get('expired_events', []))
            st.metric("Expired Events", expired_count)
    
    # Main content
    if not st.session_state.configured:
        st.markdown('<h1 class="main-header">📅 Welcome to Google Calendar Manager</h1>', unsafe_allow_html=True)
        st.markdown("### Please configure your calendar to get started")
        configure_calendar()
    else:
        if page == "🏠 Dashboard":
            show_dashboard()
        elif page == "📝 Event Management":
            show_event_management()
        elif page == "📈 Analytics":
            show_analytics()

if __name__ == "__main__":
    main()