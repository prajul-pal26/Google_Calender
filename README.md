# Google Calendar FastAPI Server

A simple FastAPI server that provides endpoints to interact with Google Calendar API using service account authentication.

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

Run the test script to verify the API endpoints:
```bash
python test_api.py
```

## Notes

- The server uses service account authentication, so make sure your service account has access to the target Google Calendar
- Datetime format should be ISO 8601 (e.g., "2025-11-13T20:00:00")
- Default timezone is "Asia/Kolkata" but can be specified in the create event request