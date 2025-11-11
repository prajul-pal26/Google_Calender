import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Google Calendar API Configuration
SERVICE_ACCOUNT_FILE = os.getenv("SERVICE_ACCOUNT_FILE", "service_account.json")
SCOPES = [os.getenv("SCOPES", "https://www.googleapis.com/auth/calendar")]

# Server Configuration
DEFAULT_TIMEZONE = os.getenv("DEFAULT_TIMEZONE", "Asia/Kolkata")
DEFAULT_HOST = os.getenv("DEFAULT_HOST", "localhost")
DEFAULT_PORT = int(os.getenv("DEFAULT_PORT", "8000"))

# Auto-Reschedule Configuration
AUTO_RESCHEDULE_AFTER_ORIGINAL_END_MINUTES = int(os.getenv("AUTO_RESCHEDULE_AFTER_ORIGINAL_END_MINUTES", "30"))
AUTO_RESCHEDULE_AFTER_PAUSE_HOURS = int(os.getenv("AUTO_RESCHEDULE_AFTER_PAUSE_HOURS", "2"))
AUTO_RESCHEDULE_SEARCH_DAYS = int(os.getenv("AUTO_RESCHEDULE_SEARCH_DAYS", "7"))

# Event Configuration
MAX_EVENTS_TO_FETCH = int(os.getenv("MAX_EVENTS_TO_FETCH", "10"))
MAX_SEARCH_RESULTS = int(os.getenv("MAX_SEARCH_RESULTS", "10"))

# Event Labeling Configuration
COMPLETED_EVENT_PREFIX = os.getenv("COMPLETED_EVENT_PREFIX", "[COMPLETED]")
MISSED_EVENT_PREFIX = os.getenv("MISSED_EVENT_PREFIX", "[MISSED]")
RESCHEDULED_EVENT_PREFIX = os.getenv("RESCHEDULED_EVENT_PREFIX", "[RESCHEDULED]")

# Time Configuration
TIME_FORMAT = os.getenv("TIME_FORMAT", "ISO 8601")  # ISO 8601 format: "2025-11-13T20:00:00"
UTC_TIMEZONE = "UTC"

# API Configuration
API_TITLE = os.getenv("API_TITLE", "Google Calendar API")
API_VERSION = os.getenv("API_VERSION", "v3")

# Debug Configuration
DEBUG_MODE = os.getenv("DEBUG_MODE", "False").lower() == "true"
LOG_AUTO_RESCHEDULE = os.getenv("LOG_AUTO_RESCHEDULE", "True").lower() == "true"

# Validation Configuration
MIN_PAUSE_DURATION_MINUTES = int(os.getenv("MIN_PAUSE_DURATION_MINUTES", "1"))
MAX_EVENT_DURATION_HOURS = int(os.getenv("MAX_EVENT_DURATION_HOURS", "24"))

# Calendar Event Limits
MAX_RECURRING_COUNT = int(os.getenv("MAX_RECURRING_COUNT", "365"))

# Feature Flags
ENABLE_AUTO_RESCHEDULE = os.getenv("ENABLE_AUTO_RESCHEDULE", "True").lower() == "true"
ENABLE_EVENT_LABELING = os.getenv("ENABLE_EVENT_LABELING", "True").lower() == "true"
ENABLE_CONFLICT_RESOLUTION = os.getenv("ENABLE_CONFLICT_RESOLUTION", "True").lower() == "true"

# Error Messages
ERROR_MESSAGES = {
    "calendar_not_configured": "Calendar not configured. Please call /configure-calendar first.",
    "no_ongoing_event": "No ongoing event found at this time",
    "no_paused_event": "No paused event found to resume",
    "failed_to_access_calendar": "Failed to access calendar",
    "failed_to_create_event": "Failed to create event",
    "failed_to_pause_event": "Failed to pause event",
    "failed_to_resume_event": "Failed to resume event",
    "failed_to_retrieve_events": "Failed to retrieve events",
    "failed_to_delete_event": "Failed to delete event",
    "failed_to_force_reschedule": "Failed to force reschedule"
}

# Success Messages
SUCCESS_MESSAGES = {
    "calendar_configured": "Calendar configured successfully for",
    "event_created": "Event created successfully",
    "event_paused": "Event paused successfully",
    "event_resumed": "Event resumed successfully",
    "events_retrieved": "Found events in calendar",
    "event_deleted": "Successfully deleted event(s) with name",
    "force_reschedule_completed": "Force reschedule completed. Check paused events to see results."
}

# Event Status
EVENT_STATUS = {
    "confirmed": "confirmed",
    "tentative": "tentative",
    "cancelled": "cancelled"
}

# Common Timezones
COMMON_TIMEZONES = [
    "UTC",
    "Asia/Kolkata",
    "America/New_York",
    "America/Los_Angeles",
    "Europe/London",
    "Europe/Paris",
    "Asia/Tokyo",
    "Australia/Sydney"
]

# Supported UTC Offsets
SUPPORTED_UTC_OFFSETS = [
    "+5:30",  # India
    "-7:00",  # USA PST
    "+0:00",  # London
    "+1:00",  # CET
    "-5:00",  # USA EST
    "+9:00",  # Japan
    "+10:00", # Australia
    "-3:00"   # Brazil
]

# Recurrence Rules
RECURRENCE_RULES = {
    "daily": "RRULE:FREQ=DAILY",
    "weekly": "RRULE:FREQ=WEEKLY",
    "monthly": "RRULE:FREQ=MONTHLY",
    "yearly": "RRULE:FREQ=YEARLY"
}

# HTTP Status Codes
HTTP_STATUS = {
    "OK": 200,
    "BAD_REQUEST": 400,
    "NOT_FOUND": 404,
    "INTERNAL_SERVER_ERROR": 500
}

# Rate Limiting (if needed in future)
RATE_LIMIT = {
    "requests_per_minute": int(os.getenv("RATE_LIMIT_RPM", "60")),
    "requests_per_hour": int(os.getenv("RATE_LIMIT_RPH", "1000"))
}

# Cache Configuration (if needed in future)
CACHE_CONFIG = {
    "enabled": os.getenv("CACHE_ENABLED", "False").lower() == "true",
    "ttl_seconds": int(os.getenv("CACHE_TTL_SECONDS", "300"))
}