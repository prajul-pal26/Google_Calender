from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
import uvicorn
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI(title="Google Calendar API")

# Load configuration from environment variables
SERVICE_ACCOUNT_FILE = os.getenv("SERVICE_ACCOUNT_FILE", "service_account.json")
SCOPES = [os.getenv("SCOPES", "https://www.googleapis.com/auth/calendar")]
DEFAULT_TIMEZONE = os.getenv("DEFAULT_TIMEZONE", "Asia/Kolkata")
DEFAULT_HOST = os.getenv("DEFAULT_HOST", "localhost")
DEFAULT_PORT = int(os.getenv("DEFAULT_PORT", "8000"))

# Global variable to store the configured calendar ID
configured_calendar_id = None

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

def get_service():
    creds = Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = build("calendar", "v3", credentials=creds)
    return service

@app.post("/configure-calendar")
async def configure_calendar(config: CalendarConfig):
    """
    Configure the Gmail calendar ID to use for creating events

        
    {
        "gmail": "cotgen00@gmail.com"
    }

    """
    global configured_calendar_id
    configured_calendar_id = config.gmail
    
    # Test if we can access this calendar
    try:
        service = get_service()
        # Try to get calendar info to verify access
        calendar = service.calendars().get(calendarId=configured_calendar_id).execute()
        return {"message": f"Calendar configured successfully for {configured_calendar_id}", "calendar_name": calendar.get("summary")}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to access calendar {configured_calendar_id}: {str(e)}")

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
    global configured_calendar_id
    
    if not configured_calendar_id:
        raise HTTPException(status_code=400, detail="Calendar not configured. Please call /configure-calendar first.")
    
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
        raise HTTPException(status_code=500, detail=f"Failed to create event: {str(e)}")

@app.get("/events")
async def get_events():
    """
    Get all event names from the configured calendar
    
    Returns a list of all events with their names, IDs, and basic timing information
    """
    global configured_calendar_id
    
    if not configured_calendar_id:
        raise HTTPException(status_code=400, detail="Calendar not configured. Please call /configure-calendar first.")
    
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
        raise HTTPException(status_code=500, detail=f"Failed to retrieve events: {str(e)}")

@app.delete("/delete-event")
async def delete_event(request: DeleteEventRequest):
    """
    Delete an event by event name from the configured calendar
    
    Example request:
    {
        "event_name": "TEST"
    }
    """
    global configured_calendar_id
    
    if not configured_calendar_id:
        raise HTTPException(status_code=400, detail="Calendar not configured. Please call /configure-calendar first.")
    
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

@app.get("/")
async def root():
    return {"message": "Google Calendar API Server", "configured_calendar": configured_calendar_id}

if __name__ == "__main__":
    uvicorn.run(app, host=DEFAULT_HOST, port=DEFAULT_PORT)