import requests
import json
from datetime import datetime, timedelta

# Base URL for the API
BASE_URL = "http://localhost:8000"

def test_pause_resume_workflow():
    """Test the complete pause/resume workflow"""
    
    print("🚀 Starting Pause/Resume Workflow Test")
    print("=" * 50)
    
    # Step 1: Configure calendar
    print("\n📅 Step 1: Configuring calendar...")
    config_data = {"gmail": "cotgen00@gmail.com"}
    response = requests.post(f"{BASE_URL}/configure-calendar", json=config_data)
    
    if response.status_code == 200:
        print("✅ Calendar configured successfully")
        print(f"Response: {response.json()}")
    else:
        print(f"❌ Failed to configure calendar: {response.text}")
        return
    
    # Step 2: Create a test event (current time + 5 minutes for 2 hours)
    print("\n📝 Step 2: Creating test event...")
    now = datetime.now()
    start_time = now + timedelta(minutes=5)
    end_time = start_time + timedelta(hours=2)
    
    event_data = {
        "event_name": "Study Session",
        "start_datetime": start_time.isoformat(),
        "end_datetime": end_time.isoformat(),
        "timezone": "Asia/Kolkata"
    }
    
    response = requests.post(f"{BASE_URL}/create-event", json=event_data)
    
    if response.status_code == 200:
        print("✅ Event created successfully")
        event_info = response.json()
        print(f"Event ID: {event_info['event_id']}")
        print(f"Event Link: {event_info['event_link']}")
    else:
        print(f"❌ Failed to create event: {response.text}")
        return
    
    # Step 3: Wait a bit, then pause the event
    print("\n⏸️ Step 3: Pausing the event...")
    print("Note: In a real scenario, you would call this when the event is actually ongoing")
    
    pause_data = {"event_name": "Study Session"}
    response = requests.post(f"{BASE_URL}/pause-event", json=pause_data)
    
    if response.status_code == 200:
        print("✅ Event paused successfully")
        pause_info = response.json()
        print(f"Paused at: {pause_info['paused_at']}")
        print(f"Remaining duration: {pause_info['remaining_duration']}")
        print(f"Completed event ID: {pause_info['completed_event_id']}")
    else:
        print(f"❌ Failed to pause event: {response.text}")
        return
    
    # Step 4: Check paused events
    print("\n📋 Step 4: Checking paused events...")
    response = requests.get(f"{BASE_URL}/paused-events")
    
    if response.status_code == 200:
        print("✅ Retrieved paused events")
        paused_info = response.json()
        print(f"Paused events: {json.dumps(paused_info, indent=2)}")
    else:
        print(f"❌ Failed to get paused events: {response.text}")
    
    # Step 5: Resume the event
    print("\n▶️ Step 5: Resuming the event...")
    resume_data = {"event_name": "Study Session"}
    response = requests.post(f"{BASE_URL}/resume-event", json=resume_data)
    
    if response.status_code == 200:
        print("✅ Event resumed successfully")
        resume_info = response.json()
        print(f"Resumed at: {resume_info['resumed_at']}")
        print(f"Ends at: {resume_info['ends_at']}")
        print(f"Duration: {resume_info['duration']}")
        print(f"Pause duration: {resume_info['pause_duration']}")
        print(f"Event ID: {resume_info['event_id']}")
        print(f"Rescheduled: {resume_info['rescheduled']}")
    else:
        print(f"❌ Failed to resume event: {response.text}")
        return
    
    # Step 6: Check paused events again (should be empty)
    print("\n📋 Step 6: Checking paused events after resume...")
    response = requests.get(f"{BASE_URL}/paused-events")
    
    if response.status_code == 200:
        print("✅ Retrieved paused events")
        paused_info = response.json()
        print(f"Paused events count: {len(paused_info['paused_events'])}")
    else:
        print(f"❌ Failed to get paused events: {response.text}")
    
    print("\n🎉 Pause/Resume workflow test completed!")

if __name__ == "__main__":
    print("Make sure the FastAPI server is running on http://localhost:8000")
    print("Press Enter to start the test...")
    input()
    
    try:
        test_pause_resume_workflow()
    except requests.exceptions.ConnectionError:
        print("❌ Connection error: Make sure the FastAPI server is running on http://localhost:8000")
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")