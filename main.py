import os
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

SERVICE_ACCOUNT_FILE = os.getenv("SERVICE_ACCOUNT_FILE", "service_account.json")
SCOPES = [os.getenv("SCOPES", "https://www.googleapis.com/auth/calendar")]

def get_service():
    creds = Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = build("calendar", "v3", credentials=creds)
    return service

def create_event():
    service = get_service()

    event = {
        "summary": "hello",
        "start": {"dateTime": "2025-11-13T20:00:00", "timeZone": "Asia/Kolkata"},
        "end": {"dateTime": "2025-11-13T20:30:00", "timeZone": "Asia/Kolkata"},
    }

    # primary calendar (your calendar)
    created_event = service.events().insert(calendarId="cotgen00@gmail.com", body=event).execute()
    print("✅ Event created:", created_event.get("htmlLink"))

if __name__ == "__main__":
    create_event()
