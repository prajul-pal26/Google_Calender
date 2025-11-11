import os
from datetime import datetime, timedelta
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from config import (
    SERVICE_ACCOUNT_FILE, SCOPES, AUTO_RESCHEDULE_AFTER_ORIGINAL_END_MINUTES,
    AUTO_RESCHEDULE_AFTER_PAUSE_HOURS, AUTO_RESCHEDULE_SEARCH_DAYS,
    COMPLETED_EVENT_PREFIX, MISSED_EVENT_PREFIX, RESCHEDULED_EVENT_PREFIX,
    MAX_EVENTS_TO_FETCH, LOG_AUTO_RESCHEDULE, UTC_TIMEZONE
)

# Global variables
configured_calendar_id = None
paused_events = {}  # {event_id: {"event_name": str, "original_event": event_data, "pause_time": datetime, "remaining_duration": timedelta}}
last_paused_event_id = None  # Track the most recently paused event

def get_service():
    """Get Google Calendar service instance"""
    creds = Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = build("calendar", "v3", credentials=creds)
    return service

def get_current_ongoing_event():
    """Get the current/ongoing event at this moment"""
    global configured_calendar_id
    
    if not configured_calendar_id:
        raise Exception("Calendar not configured")
    
    service = get_service()
    now = datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    
    # Get events happening now and in the near future
    events_result = service.events().list(
        calendarId=configured_calendar_id,
        timeMin=now,
        maxResults=MAX_EVENTS_TO_FETCH,
        singleEvents=True,
        orderBy='startTime'
    ).execute()
    
    events = events_result.get('items', [])
    current_time = datetime.now(datetime.utcnow().astimezone().tzinfo)  # Make timezone-aware
    
    for event in events:
        # Skip completed events
        if event.get('summary', '').startswith(COMPLETED_EVENT_PREFIX):
            continue
            
        start_time = datetime.fromisoformat(event['start']['dateTime'].replace('Z', '+00:00'))
        end_time = datetime.fromisoformat(event['end']['dateTime'].replace('Z', '+00:00'))
        
        # Check if current time is within the event duration
        if start_time <= current_time <= end_time:
            return event
    
    return None

def auto_reschedule_abandoned_events():
    """Reschedule events that have been paused for too long without resume"""
    global paused_events, configured_calendar_id
    
    if not configured_calendar_id or not paused_events:
        return
    
    current_time = datetime.now(datetime.utcnow().astimezone().tzinfo)  # Make timezone-aware
    service = get_service()
    events_to_reschedule = []
    
    for event_id, pause_info in list(paused_events.items()):
        original_end_time = pause_info["original_end_time"]
        pause_time = pause_info["pause_time"]
        
        # Smart timeout logic:
        # 1. If original end time + 30 minutes has passed, reschedule immediately
        # 2. OR if paused for more than 2 hours (fallback for very long pauses)
        time_since_original_end = current_time - original_end_time
        time_since_pause = current_time - pause_time
        
        should_reschedule = (
            (time_since_original_end > timedelta(minutes=AUTO_RESCHEDULE_AFTER_ORIGINAL_END_MINUTES)) or  # Configurable minutes after original end time
            (time_since_pause > timedelta(hours=AUTO_RESCHEDULE_AFTER_PAUSE_HOURS))  # Configurable hours after pause
        )
        
        if should_reschedule:
            events_to_reschedule.append((event_id, pause_info, time_since_original_end, time_since_pause))
    
    for event_id, pause_info, time_since_original_end, time_since_pause in events_to_reschedule:
        try:
            # Find available slot and reschedule
            available_start, available_end = find_available_slot(
                current_time,
                pause_info["remaining_duration"],
                service
            )
            
            # Create the rescheduled event with smart labeling
            if time_since_original_end > timedelta(minutes=AUTO_RESCHEDULE_AFTER_ORIGINAL_END_MINUTES):
                summary = f"{MISSED_EVENT_PREFIX} {pause_info['event_name']}"
            else:
                summary = f"{RESCHEDULED_EVENT_PREFIX} {pause_info['event_name']}"
            
            event_data = {
                "summary": summary,
                "start": {"dateTime": available_start.isoformat(), "timeZone": UTC_TIMEZONE},
                "end": {"dateTime": available_end.isoformat(), "timeZone": UTC_TIMEZONE},
                "description": f"Auto-rescheduled after {time_since_pause.total_seconds()/3600:.1f} hours pause. Original end time was {pause_info['original_end_time'].strftime('%Y-%m-%d %H:%M')}"
            }
            
            created_event = service.events().insert(
                calendarId=configured_calendar_id,
                body=event_data
            ).execute()
            
            # Remove from paused events
            del paused_events[event_id]
            
            # Update last_paused_event_id if this was the last one
            global last_paused_event_id
            if last_paused_event_id == event_id:
                last_paused_event_id = None
            
            if LOG_AUTO_RESCHEDULE:
                print(f"Auto-rescheduled event: {pause_info['event_name']} -> {summary}")
            
        except Exception as e:
            print(f"Failed to auto-reschedule event {event_id}: {str(e)}")

def find_available_slot(start_time: datetime, duration: timedelta, service):
    """Find the next available slot for the given duration"""
    global configured_calendar_id
    
    # Convert to ISO format for API
    time_min = start_time.isoformat()
    time_max = (start_time + timedelta(days=7)).isoformat()  # Look up to 7 days ahead
    
    # Get existing events in the range
    events_result = service.events().list(
        calendarId=configured_calendar_id,
        timeMin=time_min,
        timeMax=time_max,
        singleEvents=True,
        orderBy='startTime'
    ).execute()
    
    events = events_result.get('items', [])
    
    # Sort events by start time
    sorted_events = sorted(events, key=lambda x: x['start']['dateTime'])
    
    # Find the first available slot
    current_time = start_time
    end_time = start_time + duration
    
    for event in sorted_events:
        event_start = datetime.fromisoformat(event['start']['dateTime'].replace('Z', '+00:00'))
        event_end = datetime.fromisoformat(event['end']['dateTime'].replace('Z', '+00:00'))
        
        # If there's a gap before this event
        if current_time + duration <= event_start:
            return current_time, end_time
        
        # Move to after this event
        if event_end > current_time:
            current_time = event_end
            end_time = current_time + duration
    
    # If no suitable slot found, return the last available time
    return current_time, end_time

def create_event_in_past(event_name: str, start_time: datetime, end_time: datetime):
    """Create an event in the past to record the completed portion"""
    global configured_calendar_id
    
    service = get_service()
    
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

def get_expired_events_info():
    """Get information about expired paused events"""
    global paused_events
    
    if not paused_events:
        return []
    
    current_time = datetime.now(datetime.utcnow().astimezone().tzinfo)
    expired_events = []
    
    for event_id, pause_info in paused_events.items():
        original_end_time = pause_info["original_end_time"]
        pause_time = pause_info["pause_time"]
        
        time_since_original_end = current_time - original_end_time
        time_since_pause = current_time - pause_time
        
        # Check if event should be expired
        should_expire = (
            (time_since_original_end > timedelta(minutes=30)) or
            (time_since_pause > timedelta(hours=2))
        )
        
        if should_expire:
            expired_events.append({
                "event_id": event_id,
                "event_name": pause_info["event_name"],
                "paused_at": pause_info["pause_time"].isoformat(),
                "original_end_time": pause_info["original_end_time"].isoformat(),
                "time_since_original_end_minutes": time_since_original_end.total_seconds() / 60,
                "time_since_pause_hours": time_since_pause.total_seconds() / 3600,
                "remaining_duration": str(pause_info["remaining_duration"]),
                "will_be_labeled": "[MISSED]" if time_since_original_end > timedelta(minutes=30) else "[RESCHEDULED]"
            })
    
    return expired_events

def configure_calendar_id(gmail: str):
    """Configure the calendar ID"""
    global configured_calendar_id
    configured_calendar_id = gmail

def get_configured_calendar_id():
    """Get the configured calendar ID"""
    return configured_calendar_id

def add_paused_event(event_id: str, pause_info: dict):
    """Add an event to the paused events list"""
    global paused_events, last_paused_event_id
    paused_events[event_id] = pause_info
    last_paused_event_id = event_id

def get_paused_event(event_id: str):
    """Get a specific paused event"""
    return paused_events.get(event_id)

def get_all_paused_events():
    """Get all paused events"""
    return paused_events

def remove_paused_event(event_id: str):
    """Remove an event from the paused events list"""
    global paused_events, last_paused_event_id
    if event_id in paused_events:
        del paused_events[event_id]
    if last_paused_event_id == event_id:
        last_paused_event_id = None

def get_last_paused_event_id():
    """Get the last paused event ID"""
    return last_paused_event_id