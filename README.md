# Google Calendar FastAPI Server with Automatic Pause/Resume Functionality

A FastAPI server that provides endpoints to interact with Google Calendar API using service account authentication, with intelligent automatic pause/resume functionality for ongoing events based on current time.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Make sure you have your `service_account.json` file in the same directory.

3. Run the server:
```bash
python app.py
```

The server will start on `http://localhost:8000`

## API Endpoints

### 1. Configure Calendar
**POST** `/configure-calendar`

Configure the Gmail calendar ID to use for creating events.

**Request Body:**
```json
{
    "gmail": "your-email@gmail.com"
}
```

**Response:**
```json
{
    "message": "Calendar configured successfully for your-email@gmail.com",
    "calendar_name": "Your Calendar Name"
}
```

### 2. Create Event
**POST** `/create-event`

Create an event in the configured calendar.

**Request Body:**
```json
{
    "event_name": "Meeting with Team",
    "start_datetime": "2025-11-13T20:00:00",
    "end_datetime": "2025-11-13T20:30:00",
    "timezone": "Asia/Kolkata"
}
```

**Response:**
```json
{
    "message": "Event created successfully",
    "event_id": "event-id-here",
    "event_link": "https://calendar.google.com/calendar/event/...",
    "event_name": "Meeting with Team",
    "start_time": "2025-11-13T20:00:00",
    "end_time": "2025-11-13T20:30:00"
}
```

### 3. Root Endpoint
**GET** `/`

Get server status and currently configured calendar.

**Response:**
```json
{
    "message": "Google Calendar API Server",
    "configured_calendar": "your-email@gmail.com"
}
```

### 4. Pause Event (Automatic)
**POST** `/pause-event`

Automatically pause the currently ongoing event based on current time. No event name needed - it finds and pauses whatever event is happening right now.

**Request Body:**
```json
{}
```

**Response:**
```json
{
    "message": "Event 'Study Session' paused successfully",
    "event_name": "Study Session",
    "event_id": "current-event-id",
    "paused_at": "2025-11-11T17:30:00",
    "remaining_duration": "1:30:00",
    "completed_event_id": "completed-event-id",
    "original_end_time": "2025-11-11T19:00:00"
}
```

### 5. Resume Event (Automatic)
**POST** `/resume-event`

Automatically resume the most recently paused event. No event name needed - it resumes the last paused event.

**Request Body:**
```json
{}
```

**Response:**
```json
{
    "message": "Event 'Study Session' resumed successfully",
    "event_name": "Study Session",
    "resumed_at": "2025-11-11T17:35:00",
    "ends_at": "2025-11-11T19:05:00",
    "duration": "1:30:00",
    "pause_duration": "0:05:00",
    "event_id": "resumed-event-id",
    "event_link": "https://calendar.google.com/calendar/event/...",
    "rescheduled": false
}
```

### 6. Get Paused Events
**GET** `/paused-events`

Get all currently paused events with detailed information.

**Response:**
```json
{
    "message": "Found 1 paused events",
    "paused_events": [
        {
            "event_id": "event-id-here",
            "event_name": "Study Session",
            "paused_at": "2025-11-11T17:30:00",
            "remaining_duration": "1:30:00",
            "original_end_time": "2025-11-11T19:00:00",
            "is_last_paused": true
        }
    ],
    "last_paused_event_id": "event-id-here"
}
```

### 7. Get All Events
**GET** `/events`

Get all event names from the configured calendar.

**Response:**
```json
{
    "message": "Found 5 events in calendar",
    "total_events": 5,
    "events": [
        {
            "event_id": "event-id-1",
            "event_name": "Meeting with Team",
            "start_time": "2025-11-13T20:00:00",
            "end_time": "2025-11-13T20:30:00",
            "status": "confirmed"
        }
    ]
}
```

### 8. Delete Event
**DELETE** `/delete-event`

Delete an event by event name from the configured calendar.

**Request Body:**
```json
{
    "event_name": "TEST"
}
```

## Automatic Pause/Resume Workflow

The pause/resume system provides intelligent event management based on current time:

### How It Works:

1. **Automatic Pause**: When you hit pause:
   - The system automatically finds whatever event is happening RIGHT NOW
   - The completed portion is saved as a separate event with "[COMPLETED]" prefix
   - The original event is deleted
   - Remaining time is tracked and stored

2. **Automatic Resume**: When you hit resume:
   - The system resumes the LAST paused event automatically
   - It tries to resume immediately (current time)
   - If the current time slot is occupied, it finds the next available slot
   - The event duration includes the original remaining time

3. **Smart Time Management**:
   - If you take a 1-hour break, the event automatically extends by 1 hour
   - If the extended time conflicts with other events, it finds the next available slot
   - All time calculations are done automatically

4. **Corner Case Handling**:
   - If you pause but never resume, the system auto-reschedules after 2 hours
   - Abandoned events are marked as "[RESCHEDULED]" and placed in available slots
   - No manual intervention needed for abandoned pauses

### Key Features:

- **No Event Names Needed**: The system works based on current time, not event names
- **Always Current**: Pause always affects the event happening right now
- **Smart Rescheduling**: Automatically finds available slots when there are conflicts
- **Time Tracking**: Accurately tracks completed vs remaining time
- **Abandoned Event Recovery**: Auto-reschedules events left paused too long

## Usage Example

1. First, configure the calendar:
```bash
curl -X POST "http://localhost:8000/configure-calendar" \
     -H "Content-Type: application/json" \
     -d '{"gmail": "cotgen00@gmail.com"}'
```

2. Then create an event:
```bash
curl -X POST "http://localhost:8000/create-event" \
     -H "Content-Type: application/json" \
     -d '{
           "event_name": "Team Meeting",
           "start_datetime": "2025-11-13T20:00:00",
           "end_datetime": "2025-11-13T20:30:00",
           "timezone": "Asia/Kolkata"
         }'
```

## Testing

### Basic API Test
Run the basic test script to verify the API endpoints:
```bash
python test_api.py
```

### Pause/Resume Workflow Test
Run the pause/resume test script to test the complete workflow:
```bash
python test_pause_resume.py
```

This test will:
1. Configure the calendar
2. Create a test event
3. Pause the event (simulating taking a break)
4. Check paused events
5. Resume the event (with automatic time adjustment)
6. Verify the event is properly rescheduled

## Notes

- The server uses service account authentication, so make sure your service account has access to the target Google Calendar
- Datetime format should be ISO 8601 (e.g., "2025-11-13T20:00:00")
- Default timezone is "Asia/Kolkata" but can be specified in the create event request
- Paused events are stored in memory (will be lost if server restarts)
- Completed portions are saved as separate events with "[COMPLETED]" prefix
- The system automatically handles time conflicts by finding the next available slot
- All time calculations are done in UTC to avoid timezone issues

## Advanced Features

### Smart Time Management
- **Automatic Extension**: When you resume after a break, the event automatically extends by the break duration
- **Conflict Resolution**: If the extended time conflicts with other events, the system finds the next available slot
- **Completed Tracking**: All completed portions are tracked as separate events for accurate time logging

### Event State Management
- **Pause State**: Events can be paused and resumed with full state preservation
- **Duration Tracking**: Remaining duration is accurately calculated and preserved
- **Time Zone Handling**: All time operations are handled in UTC with proper timezone conversion