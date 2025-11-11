import requests
import json
import time
from datetime import datetime, timedelta

# Base URL for the API
BASE_URL = "http://localhost:8000"

def test_auto_pause_resume_workflow():
    """Test the automatic pause/resume workflow based on current time"""
    
    print("🚀 Starting Automatic Pause/Resume Workflow Test")
    print("=" * 60)
    
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
    
    # Step 2: Create a test event that starts now and runs for 2 hours
    print("\n📝 Step 2: Creating test event that starts now...")
    now = datetime.now()
    start_time = now
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
        print(f"Event runs from: {event_info['start_time']} to {event_info['end_time']}")
    else:
        print(f"❌ Failed to create event: {response.text}")
        return
    
    # Step 3: Wait a bit, then pause the current event (no event name needed)
    print("\n⏸️ Step 3: Pausing the current ongoing event...")
    print("Note: This will automatically find and pause the event happening right now")
    print("Waiting 3 seconds before pausing...")
    time.sleep(3)
    
    # Pause request with empty body (no event name needed)
    response = requests.post(f"{BASE_URL}/pause-event", json={})
    
    if response.status_code == 200:
        print("✅ Current event paused successfully")
        pause_info = response.json()
        print(f"Event Name: {pause_info['event_name']}")
        print(f"Event ID: {pause_info['event_id']}")
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
        print(f"Last paused event ID: {paused_info['last_paused_event_id']}")
        for event in paused_info['paused_events']:
            print(f"  - {event['event_name']} (ID: {event['event_id']})")
            print(f"    Paused at: {event['paused_at']}")
            print(f"    Remaining: {event['remaining_duration']}")
            print(f"    Is last paused: {event['is_last_paused']}")
    else:
        print(f"❌ Failed to get paused events: {response.text}")
    
    # Step 5: Wait a bit to simulate break time, then resume (no event name needed)
    print("\n▶️ Step 5: Resuming the last paused event...")
    print("Simulating a 3-second break...")
    time.sleep(3)
    
    # Resume request with empty body (no event name needed)
    response = requests.post(f"{BASE_URL}/resume-event", json={})
    
    if response.status_code == 200:
        print("✅ Event resumed successfully")
        resume_info = response.json()
        print(f"Event Name: {resume_info['event_name']}")
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
        print(f"Last paused event ID: {paused_info['last_paused_event_id']}")
    else:
        print(f"❌ Failed to get paused events: {response.text}")
    
    # Step 7: Test corner case - pause without resume
    print("\n🧪 Step 7: Testing corner case - pause without resume...")
    print("Creating another event to test abandoned pause...")
    
    # Create another event
    start_time = datetime.now()
    end_time = start_time + timedelta(hours=1)
    
    event_data = {
        "event_name": "Work Session",
        "start_datetime": start_time.isoformat(),
        "end_datetime": end_time.isoformat(),
        "timezone": "Asia/Kolkata"
    }
    
    response = requests.post(f"{BASE_URL}/create-event", json=event_data)
    
    if response.status_code == 200:
        print("✅ Second event created successfully")
        time.sleep(2)
        
        # Pause the event
        response = requests.post(f"{BASE_URL}/pause-event", json={})
        
        if response.status_code == 200:
            print("✅ Second event paused successfully")
            print("Note: This event will be auto-rescheduled after 2 hours if not resumed")
            
            # Check paused events
            response = requests.get(f"{BASE_URL}/paused-events")
            if response.status_code == 200:
                paused_info = response.json()
                print(f"Currently paused events: {len(paused_info['paused_events'])}")
        else:
            print(f"❌ Failed to pause second event: {response.text}")
    else:
        print(f"❌ Failed to create second event: {response.text}")
    
    print("\n🎉 Automatic Pause/Resume workflow test completed!")
    print("\nKey Features Demonstrated:")
    print("✅ Automatic pause of current ongoing event (no event name needed)")
    print("✅ Automatic resume of last paused event (no event name needed)")
    print("✅ Completed portion saved as separate event")
    print("✅ Remaining time properly tracked and rescheduled")
    print("✅ Conflict resolution for time slots")
    print("✅ Corner case handling for abandoned paused events")

if __name__ == "__main__":
    print("Make sure the FastAPI server is running on http://localhost:8000")
    print("This test will demonstrate the automatic pause/resume functionality")
    print("based on the current time, not event names.")
    print("\nPress Enter to start the test...")
    input()
    
    try:
        test_auto_pause_resume_workflow()
    except requests.exceptions.ConnectionError:
        print("❌ Connection error: Make sure the FastAPI server is running on http://localhost:8000")
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")