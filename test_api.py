import requests
import json

# Base URL for the FastAPI server
BASE_URL = "http://localhost:8000"

def test_configure_calendar():
    """Test the configure calendar endpoint

    """
    url = f"{BASE_URL}/configure-calendar"
    data = {
        "gmail": "cotgen00@gmail.com"
    }
    
    try:
        response = requests.post(url, json=data)
        print("Configure Calendar Response:")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        print("-" * 50)
        return response.status_code == 200
    except Exception as e:
        print(f"Error configuring calendar: {e}")
        return False

def test_create_event():
    """Test the create event endpoint"""
    url = f"{BASE_URL}/create-event"
    data = {
        "event_name": "Test Meeting",
        "start_datetime": "2025-11-13T20:00:00",
        "end_datetime": "2025-11-13T20:30:00",
        "timezone": "Asia/Kolkata"
    }
    
    try:
        response = requests.post(url, json=data)
        print("Create Event Response:")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        print("-" * 50)
        return response.status_code == 200
    except Exception as e:
        print(f"Error creating event: {e}")
        return False

def test_create_event_with_timezone():
    """Test the create event endpoint with different timezone"""
    url = f"{BASE_URL}/create-event"
    data = {
        "event_name": "NYC Meeting",
        "start_datetime": "2025-11-13T14:00:00",
        "end_datetime": "2025-11-13T15:00:00",
        "timezone": "America/New_York",
        "recurrence": [
            "RRULE:FREQ=WEEKLY;COUNT=4"
        ]
    }
    
    try:
        response = requests.post(url, json=data)
        print("Create Event with Timezone Response:")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        print("-" * 50)
        return response.status_code == 200
    except Exception as e:
        print(f"Error creating event with timezone: {e}")
        return False

def test_create_event_with_utc_offset():
    """Test the create event endpoint with UTC offset"""
    url = f"{BASE_URL}/create-event"
    data = {
        "event_name": "India Meeting",
        "start_datetime": "2025-11-13T10:00:00",
        "end_datetime": "2025-11-13T11:00:00",
        "utc_offset": "+5:30",
        "recurrence": [
            "RRULE:FREQ=DAILY;COUNT=5"
        ]
    }
    
    try:
        response = requests.post(url, json=data)
        print("Create Event with UTC Offset Response:")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        print("-" * 50)
        return response.status_code == 200
    except Exception as e:
        print(f"Error creating event with UTC offset: {e}")
        return False

def test_create_event_london_utc_offset():
    """Test the create event endpoint with London UTC offset"""
    url = f"{BASE_URL}/create-event"
    data = {
        "event_name": "London Meeting",
        "start_datetime": "2025-11-13T12:00:00",
        "end_datetime": "2025-11-13T13:00:00",
        "utc_offset": "+0:00",
        "recurrence": [
            "RRULE:FREQ=WEEKLY;BYDAY=MO,WE,FR"
        ]
    }
    
    try:
        response = requests.post(url, json=data)
        print("Create Event with London UTC Offset Response:")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        print("-" * 50)
        return response.status_code == 200
    except Exception as e:
        print(f"Error creating event with London UTC offset: {e}")
        return False

def test_get_events():
    """Test the get events endpoint"""
    url = f"{BASE_URL}/events"
    
    try:
        response = requests.get(url)
        print("Get Events Response:")
        print(f"Status Code: {response.status_code}")
        response_data = response.json()
        print(f"Total Events: {response_data.get('total_events', 0)}")
        print("Events:")
        for event in response_data.get('events', []):
            print(f"  - {event.get('event_name')} (ID: {event.get('event_id')})")
        print("-" * 50)
        return response.status_code == 200
    except Exception as e:
        print(f"Error getting events: {e}")
        return False

def test_delete_event():
    """Test the delete event endpoint"""
    url = f"{BASE_URL}/delete-event"
    data = {
        "event_name": "TEST"
    }
    
    try:
        response = requests.delete(url, json=data)
        print("Delete Event Response:")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        print("-" * 50)
        return response.status_code == 200
    except Exception as e:
        print(f"Error deleting event: {e}")
        return False

def test_create_recurring_event():
    """Test the create event endpoint with recurrence"""
    url = f"{BASE_URL}/create-event"
    data = {
        "event_name": "Daily Standup Meeting",
        "start_datetime": "2025-11-13T09:00:00",
        "end_datetime": "2025-11-13T09:15:00",
        "timezone": "Asia/Kolkata",
        "recurrence": [
            "RRULE:FREQ=DAILY;COUNT=7"
        ]
    }
    
    try:
        response = requests.post(url, json=data)
        print("Create Recurring Event Response:")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        print("-" * 50)
        return response.status_code == 200
    except Exception as e:
        print(f"Error creating recurring event: {e}")
        return False

def test_root():
    """Test the root endpoint"""
    url = f"{BASE_URL}/"
    
    try:
        response = requests.get(url)
        print("Root Endpoint Response:")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        print("-" * 50)
        return response.status_code == 200
    except Exception as e:
        print(f"Error accessing root endpoint: {e}")
        return False

if __name__ == "__main__":
    print("Testing Google Calendar API Server")
    print("=" * 50)
    
    # Test root endpoint
    test_root()
    
    # Test configure calendar
    if test_configure_calendar():
        # Test create event only if calendar configuration succeeded
        test_create_event()
        # Test create recurring event
        test_create_recurring_event()
        # Test create event with different timezone
        test_create_event_with_timezone()
        # Test create event with UTC offset (India)
        test_create_event_with_utc_offset()
        # Test create event with London UTC offset
        test_create_event_london_utc_offset()
        # Test get all events
        test_get_events()
        # Test delete event
        test_delete_event()
    else:
        print("Skipping event creation test due to calendar configuration failure")