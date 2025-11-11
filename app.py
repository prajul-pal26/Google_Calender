from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import uvicorn
from datetime import datetime, timedelta
from config import (
    DEFAULT_TIMEZONE, DEFAULT_HOST, DEFAULT_PORT, API_TITLE,
    ERROR_MESSAGES, SUCCESS_MESSAGES, HTTP_STATUS
)
from utils import (
    get_service, get_current_ongoing_event, auto_reschedule_abandoned_events,
    find_available_slot, create_event_in_past, get_expired_events_info,
    configure_calendar_id, get_configured_calendar_id, add_paused_event,
    get_paused_event, get_all_paused_events, remove_paused_event,
    get_last_paused_event_id
)

app = FastAPI(title=API_TITLE)

# Pydantic models for requests
class CalendarConfig(BaseModel):
    gmail: str

class DeleteEventRequest(BaseModel):
    event_name: str

class EventRequest(BaseModel):
    event_name: str
    start_datetime: str
    end_datetime: str
    timezone: str = DEFAULT_TIMEZONE
    utc_offset: Optional[str] = None  # Format: "+5:30", "-7:00", "+0:00", etc.
    recurrence: Optional[list] = None

class PauseEventRequest(BaseModel):
    pass  # No event name needed - will pause current ongoing event

class ResumeEventRequest(BaseModel):
    pass  # No event name needed - will resume last paused event

@app.post("/configure-calendar")
async def configure_calendar(config: CalendarConfig):
    """
    Configure the Gmail calendar ID to use for creating events

        
    {
        "gmail": "cotgen00@gmail.com"
    }

    """
    try:
        configure_calendar_id(config.gmail)
        
        # Test if we can access this calendar
        service = get_service()
        # Try to get calendar info to verify access
        calendar = service.calendars().get(calendarId=config.gmail).execute()
        return {"message": f"{SUCCESS_MESSAGES['calendar_configured']} {config.gmail}", "calendar_name": calendar.get("summary")}
    except Exception as e:
        raise HTTPException(status_code=HTTP_STATUS["BAD_REQUEST"], detail=f"{ERROR_MESSAGES['failed_to_access_calendar']} {config.gmail}: {str(e)}")

@app.post("/create-event")
async def create_event(event: EventRequest):
    """
    Create an event in the configured calendar
    
    {
        "event_name": "TEST",
        "start_datetime": "2025-11-15T20:00:00",
        "end_datetime": "2025-11-15T21:00:00",
        "timezone": "Asia/Kolkata",
        "utc_offset": "+5:30",
        "recurrence": [
            "RRULE:FREQ=DAILY;COUNT=7"
        ]
        }
    Supported formats:
    - Timezone names: "UTC", "Asia/Kolkata", "America/New_York", "Europe/London", etc.
    - UTC offsets: "+5:30" (India), "-7:00" (USA PST), "+0:00" (London), "+1:00" (CET), etc.
    """
    configured_calendar_id = get_configured_calendar_id()
    
    if not configured_calendar_id:
        raise HTTPException(status_code=HTTP_STATUS["BAD_REQUEST"], detail=ERROR_MESSAGES["calendar_not_configured"])
    
    try:
        service = get_service()
        
        # Determine which timezone to use
        timezone_to_use = event.timezone
        if event.utc_offset:
            # Convert UTC offset to timezone format
            # Google Calendar accepts UTC offsets in format like "UTC+05:30" or "UTC-07:00"
            timezone_to_use = f"UTC{event.utc_offset}"
        
        event_data = {
            "summary": event.event_name,
            "start": {"dateTime": event.start_datetime, "timeZone": timezone_to_use},
            "end": {"dateTime": event.end_datetime, "timeZone": timezone_to_use},
        }
        
        # Add recurrence if provided
        if event.recurrence:
            event_data["recurrence"] = event.recurrence
        
        created_event = service.events().insert(
            calendarId=configured_calendar_id, 
            body=event_data
        ).execute()
        
        return {
            "message": "Event created successfully",
            "event_id": created_event.get("id"),
            "event_link": created_event.get("htmlLink"),
            "event_name": event.event_name,
            "start_time": event.start_datetime,
            "end_time": event.end_datetime,
            "timezone_used": timezone_to_use,
            "original_timezone": event.timezone,
            "utc_offset": event.utc_offset,
            "recurrence": event.recurrence
        }
        
    except Exception as e:
        raise HTTPException(status_code=HTTP_STATUS["INTERNAL_SERVER_ERROR"], detail=f"{ERROR_MESSAGES['failed_to_create_event']}: {str(e)}")

@app.get("/events")
async def get_events():
    """
    Get all event names from the configured calendar
    
    Returns a list of all events with their names, IDs, and basic timing information
    """
    configured_calendar_id = get_configured_calendar_id()
    
    if not configured_calendar_id:
        raise HTTPException(status_code=HTTP_STATUS["BAD_REQUEST"], detail=ERROR_MESSAGES["calendar_not_configured"])
    
    try:
        service = get_service()
        
        # Get all events from the calendar
        events_result = service.events().list(
            calendarId=configured_calendar_id,
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        
        events = events_result.get('items', [])
        event_list = []
        
        # Extract event information
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
        raise HTTPException(status_code=HTTP_STATUS["INTERNAL_SERVER_ERROR"], detail=f"{ERROR_MESSAGES['failed_to_retrieve_events']}: {str(e)}")

@app.delete("/delete-event")
async def delete_event(request: DeleteEventRequest):
    """
    Delete an event by event name from the configured calendar
    
    Example request:
    {
        "event_name": "TEST"
    }
    """
    configured_calendar_id = get_configured_calendar_id()
    
    if not configured_calendar_id:
        raise HTTPException(status_code=HTTP_STATUS["BAD_REQUEST"], detail=ERROR_MESSAGES["calendar_not_configured"])
    
    try:
        service = get_service()
        
        # First, list all events to find the one with the matching name
        events_result = service.events().list(
            calendarId=configured_calendar_id,
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        
        events = events_result.get('items', [])
        deleted_events = []
        
        # Find and delete events with matching name
        for event in events:
            if event.get('summary') == request.event_name:
                # Delete the event
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
                "message": f"No events found with name '{request.event_name}'",
                "deleted_count": 0
            }
        
        return {
            "message": f"Successfully deleted {len(deleted_events)} event(s) with name '{request.event_name}'",
            "deleted_count": len(deleted_events),
            "deleted_events": deleted_events
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete event: {str(e)}")

@app.post("/pause-event")
async def pause_event(request: PauseEventRequest):
    """
    Pause the currently ongoing event automatically
    
    No parameters needed - will find and pause the event happening right now
    """
    configured_calendar_id = get_configured_calendar_id()
    
    if not configured_calendar_id:
        raise HTTPException(status_code=HTTP_STATUS["BAD_REQUEST"], detail=ERROR_MESSAGES["calendar_not_configured"])
    
    try:
        # Auto-reschedule any abandoned events first
        auto_reschedule_abandoned_events()
        
        # Get the current ongoing event
        current_event = get_current_ongoing_event()
        
        if not current_event:
            raise HTTPException(status_code=404, detail="No ongoing event found at this time")
        
        service = get_service()
        event_name = current_event.get('summary', 'Unknown Event')
        
        # Get event timing details
        start_time = datetime.fromisoformat(current_event['start']['dateTime'].replace('Z', '+00:00'))
        original_end_time = datetime.fromisoformat(current_event['end']['dateTime'].replace('Z', '+00:00'))
        current_time = datetime.now(start_time.tzinfo)  # Use same timezone as event
        
        # Calculate remaining duration
        remaining_duration = original_end_time - current_time
        
        # Create a completed event for the portion that was done
        completed_event = create_event_in_past(
            event_name,
            start_time,
            current_time
        )
        
        # Delete the original event
        service.events().delete(
            calendarId=configured_calendar_id,
            eventId=current_event['id']
        ).execute()
        
        # Store pause information using event ID as key
        pause_info = {
            "event_name": event_name,
            "original_event": current_event,
            "pause_time": current_time,
            "remaining_duration": remaining_duration,
            "original_end_time": original_end_time
        }
        
        add_paused_event(current_event['id'], pause_info)
        
        return {
            "message": f"Event '{event_name}' paused successfully",
            "event_name": event_name,
            "event_id": current_event['id'],
            "paused_at": current_time.isoformat(),
            "remaining_duration": str(remaining_duration),
            "completed_event_id": completed_event.get("id"),
            "original_end_time": original_end_time.isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to pause event: {str(e)}")

@app.post("/resume-event")
async def resume_event(request: ResumeEventRequest):
    """
    Resume the most recently paused event automatically
    
    No parameters needed - will resume the last paused event
    """
    configured_calendar_id = get_configured_calendar_id()
    
    if not configured_calendar_id:
        raise HTTPException(status_code=HTTP_STATUS["BAD_REQUEST"], detail=ERROR_MESSAGES["calendar_not_configured"])
    
    try:
        # Check if there's a paused event
        last_paused_event_id = get_last_paused_event_id()
        if not last_paused_event_id:
            raise HTTPException(status_code=404, detail="No paused event found to resume")
        
        pause_info = get_paused_event(last_paused_event_id)
        if not pause_info:
            raise HTTPException(status_code=404, detail="No paused event found to resume")
        
        current_time = datetime.now(pause_info["pause_time"].tzinfo)  # Use same timezone as paused event
        
        # Calculate how long the pause was
        pause_duration = current_time - pause_info["pause_time"]
        
        service = get_service()
        
        # Try to resume immediately (current time)
        proposed_start_time = current_time
        proposed_end_time = proposed_start_time + pause_info["remaining_duration"]
        
        # Check if the slot is available
        available_start, available_end = find_available_slot(
            proposed_start_time,
            pause_info["remaining_duration"],
            service
        )
        
        # Create the resumed event
        event_data = {
            "summary": pause_info["event_name"],
            "start": {"dateTime": available_start.isoformat(), "timeZone": "UTC"},
            "end": {"dateTime": available_end.isoformat(), "timeZone": "UTC"},
        }
        
        created_event = service.events().insert(
            calendarId=configured_calendar_id,
            body=event_data
        ).execute()
        
        # Remove from paused events
        remove_paused_event(last_paused_event_id)
        
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
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to resume event: {str(e)}")

@app.get("/paused-events")
async def get_paused_events():
    """
    Get all currently paused events
    """
    paused_events = get_all_paused_events()
    last_paused_event_id = get_last_paused_event_id()
    
    if not paused_events:
        return {"message": "No paused events", "paused_events": [], "last_paused_event_id": None}
    
    paused_list = []
    for event_id, pause_info in paused_events.items():
        paused_list.append({
            "event_id": event_id,
            "event_name": pause_info["event_name"],
            "paused_at": pause_info["pause_time"].isoformat(),
            "remaining_duration": str(pause_info["remaining_duration"]),
            "original_end_time": pause_info["original_end_time"].isoformat(),
            "is_last_paused": event_id == last_paused_event_id
        })
    
    return {
        "message": f"Found {len(paused_list)} paused events",
        "paused_events": paused_list,
        "last_paused_event_id": last_paused_event_id
    }

@app.get("/check-expired-events")
async def check_expired_events():
    """
    Check for paused events that should be auto-rescheduled
    """
    expired_events = get_expired_events_info()
    paused_events = get_all_paused_events()
    
    return {
        "message": f"Found {len(expired_events)} expired paused events",
        "expired_events": expired_events,
        "total_paused_events": len(paused_events)
    }

@app.post("/force-reschedule-expired")
async def force_reschedule_expired():
    """
    Manually trigger rescheduling of all expired paused events
    """
    configured_calendar_id = get_configured_calendar_id()
    
    if not configured_calendar_id:
        raise HTTPException(status_code=400, detail="Calendar not configured. Please call /configure-calendar first.")
    
    try:
        # Run the auto-reschedule logic
        auto_reschedule_abandoned_events()
        
        return {
            "message": "Force reschedule completed. Check paused events to see results.",
            "note": "Expired events have been rescheduled and removed from paused list."
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to force reschedule: {str(e)}")

@app.get("/")
async def root():
    configured_calendar_id = get_configured_calendar_id()
    return {"message": "Google Calendar API Server", "configured_calendar": configured_calendar_id}

if __name__ == "__main__":
    uvicorn.run(app, host=DEFAULT_HOST, port=DEFAULT_PORT)