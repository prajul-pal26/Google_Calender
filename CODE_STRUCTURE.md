# Google Calendar API - Code Structure

This document explains the organization of the codebase and the separation of concerns.

## File Structure

```
├── app.py              # FastAPI endpoints (8 endpoints)
├── utils.py            # Helper functions (12 functions)
├── config.py           # Configuration settings (50+ config variables)
├── main.py             # Simple script for basic event creation
├── test_api.py         # Basic API testing
├── test_auto_pause_resume.py  # Advanced pause/resume testing
├── requirements.txt    # Python dependencies
├── .gitignore         # Git ignore file
├── README.md          # Documentation
└── CODE_STRUCTURE.md  # This file
```

## File Responsibilities

### 🚀 **app.py** - API Endpoints (8 endpoints)
**Only contains FastAPI route handlers and request/response models**

#### Endpoints:
1. `POST /configure-calendar` - Configure Gmail calendar
2. `POST /create-event` - Create new calendar event
3. `GET /events` - Get all events from calendar
4. `DELETE /delete-event` - Delete event by name
5. `POST /pause-event` - Pause current ongoing event
6. `POST /resume-event` - Resume last paused event
7. `GET /paused-events` - Get all paused events
8. `GET /check-expired-events` - Check events that need rescheduling
9. `POST /force-reschedule-expired` - Manually trigger rescheduling
10. `GET /` - Root endpoint for server status

#### Request Models:
- `CalendarConfig`
- `DeleteEventRequest`
- `EventRequest`
- `PauseEventRequest`
- `ResumeEventRequest`

### 🔧 **utils.py** - Helper Functions (12 functions)
**Contains all business logic and data manipulation**

#### Core Functions:
1. `get_service()` - Get Google Calendar service instance
2. `get_current_ongoing_event()` - Find event happening right now
3. `auto_reschedule_abandoned_events()` - Handle forgotten paused events
4. `find_available_slot()` - Find next available time slot
5. `create_event_in_past()` - Create completed event record

#### State Management Functions:
6. `configure_calendar_id()` - Set calendar ID
7. `get_configured_calendar_id()` - Get calendar ID
8. `add_paused_event()` - Add event to paused list
9. `get_paused_event()` - Get specific paused event
10. `get_all_paused_events()` - Get all paused events
11. `remove_paused_event()` - Remove from paused list
12. `get_last_paused_event_id()` - Get last paused event ID

#### Global Variables:
- `configured_calendar_id` - Current calendar ID
- `paused_events` - Dictionary of paused events
- `last_paused_event_id` - Track most recent pause

### ⚙️ **config.py** - Configuration (50+ config variables)
**Centralized configuration with environment variable support**

#### Categories:
- **Google Calendar API**: Service account, scopes
- **Server**: Host, port, timezone
- **Auto-Reschedule**: Timeouts, search days
- **Event**: Limits, prefixes, labels
- **API**: Title, version, status codes
- **Messages**: Error and success messages
- **Features**: Feature flags
- **Rate Limiting**: Future-proof rate limits
- **Cache**: Future-proof cache settings

#### Key Configurations:
```python
# Auto-Reschedule Timing
AUTO_RESCHEDULE_AFTER_ORIGINAL_END_MINUTES = 30
AUTO_RESCHEDULE_AFTER_PAUSE_HOURS = 2

# Event Labels
COMPLETED_EVENT_PREFIX = "[COMPLETED]"
MISSED_EVENT_PREFIX = "[MISSED]"
RESCHEDULED_EVENT_PREFIX = "[RESCHEDULED]"

# Error Messages
ERROR_MESSAGES = {
    "calendar_not_configured": "Calendar not configured...",
    "no_ongoing_event": "No ongoing event found...",
    # ... more messages
}
```

## Data Flow

### Pause Event Flow:
```
1. POST /pause-event (app.py)
   ↓
2. get_current_ongoing_event() (utils.py)
   ↓
3. create_event_in_past() (utils.py)
   ↓
4. add_paused_event() (utils.py)
   ↓
5. Return response (app.py)
```

### Resume Event Flow:
```
1. POST /resume-event (app.py)
   ↓
2. get_last_paused_event_id() (utils.py)
   ↓
3. get_paused_event() (utils.py)
   ↓
4. find_available_slot() (utils.py)
   ↓
5. remove_paused_event() (utils.py)
   ↓
6. Return response (app.py)
```

### Auto-Reschedule Flow:
```
1. auto_reschedule_abandoned_events() (utils.py)
   ↓
2. Check timeout conditions (config.py values)
   ↓
3. find_available_slot() (utils.py)
   ↓
4. Create new event with labels (config.py prefixes)
   ↓
5. remove_paused_event() (utils.py)
```

## Benefits of This Structure

### 🎯 **Separation of Concerns**
- **app.py**: Only handles HTTP requests/responses
- **utils.py**: Only handles business logic
- **config.py**: Only handles configuration

### 🔧 **Maintainability**
- Easy to modify business logic without touching endpoints
- Easy to add new endpoints without changing logic
- Centralized configuration management

### 🧪 **Testability**
- Can test utils functions independently
- Can mock configuration easily
- Clear separation for unit testing

### 📈 **Scalability**
- Easy to add new helper functions
- Easy to add new configuration options
- Clear structure for future features

### 🔄 **Reusability**
- Utils functions can be used by multiple endpoints
- Configuration can be shared across modules
- Clear interfaces between components

## Environment Variables

Create a `.env` file to customize behavior:

```bash
# Server Configuration
DEFAULT_TIMEZONE=Asia/Kolkata
DEFAULT_HOST=localhost
DEFAULT_PORT=8000

# Auto-Reschedule Timing
AUTO_RESCHEDULE_AFTER_ORIGINAL_END_MINUTES=30
AUTO_RESCHEDULE_AFTER_PAUSE_HOURS=2

# Event Labels
COMPLETED_EVENT_PREFIX=[COMPLETED]
MISSED_EVENT_PREFIX=[MISSED]
RESCHEDULED_EVENT_PREFIX=[RESCHEDULED]

# Feature Flags
ENABLE_AUTO_RESCHEDULE=True
ENABLE_EVENT_LABELING=True
DEBUG_MODE=False
```

## Summary

- **8 API endpoints** in `app.py`
- **12 helper functions** in `utils.py`
- **50+ configuration options** in `config.py`
- **Clear separation** between HTTP handling, business logic, and configuration
- **Easy to maintain** and extend
- **Environment-based configuration** for different deployment scenarios