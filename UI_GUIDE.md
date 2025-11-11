# 📅 Google Calendar Pause/Resume Manager - User Guide

## 🚀 Quick Start

### 1. Installation
```bash
pip install -r requirements.txt
```

### 2. Start the Application
```bash
python start.py
```

This will start both:
- **FastAPI Server** at http://localhost:8000
- **Streamlit UI** at http://localhost:8501

### 3. Open Your Browser
Go to http://localhost:8501 to access the beautiful web interface!

---

## 🎛️ Interface Overview

### 🏠 Dashboard (Main Page)

The dashboard gives you a complete overview of your calendar status and quick actions:

#### **Quick Actions Section**
- **⏸️ Pause Current Event**: Instantly pause whatever event is happening right now
- **▶️ Resume Last Event**: Resume the most recently paused event
- **🔄 Refresh All**: Refresh all data and status

#### **Status Cards**
- **Total Events**: Number of events in your calendar
- **Paused Events**: Currently paused events
- **Expired Events**: Events that need rescheduling
- **Calendar ID**: Your configured Gmail address

#### **Currently Paused Events**
Shows all paused events with:
- Event name and pause time
- Remaining duration
- Original end time
- Resume button for each event

#### **Expired Events**
Shows events that have been paused too long:
- Time since original end time
- Time since pause
- **🔄 Force Reschedule All** button to handle all expired events

---

## 📝 Event Management

### Create New Event
1. Go to **Event Management** → **Create Event**
2. Fill in the details:
   - **Event Name**: "Study Session", "Meeting", etc.
   - **Start Date/Time**: When the event begins
   - **End Date/Time**: When the event ends
   - **Timezone**: Your local timezone
3. Click **Create Event**

### View All Events
1. Go to **Event Management** → **View Events**
2. Click **Refresh Events** to load your calendar
3. See all events in a table format
4. **Event Timeline** visualization shows your schedule

### Delete Events
1. Go to **Event Management** → **Delete Event**
2. Enter the exact event name
3. ⚠️ **Confirm deletion** with checkbox
4. Click **Delete Event**

---

## 📈 Analytics & Insights

### Event Statistics
- **Total Events**: All events in calendar
- **Completed Events**: Events marked as [COMPLETED]
- **Missed Events**: Events marked as [MISSED]
- **Rescheduled Events**: Events marked as [RESCHEDULED]
- **Active Events**: Currently active events
- **Paused Events**: Currently paused events

### Event Status Distribution
- Bar chart showing the breakdown of event statuses
- Visual representation of your calendar health

### Paused Events Analysis
- Detailed breakdown of each paused event
- Pause duration
- Remaining time
- Progress indicators

---

## 🎯 Daily Use Workflow

### **For Study Sessions/Work**

1. **Start Your Day**: Create your study/work events in advance
2. **During Study**: When you need a break:
   - Click **⏸️ Pause Current Event** on the dashboard
   - Take your break
   - Click **▶️ Resume Last Event** when you're back
3. **Automatic Time Management**: The system automatically:
   - Extends your event by the break duration
   - Finds available slots if there are conflicts
   - Saves completed portions as separate events

### **For Meetings/Appointments**

1. **Before Meeting**: Create the meeting event
2. **During Meeting**: If meeting runs long or needs pause:
   - Use pause/resume as needed
3. **After Meeting**: Check analytics to see time spent

### **For Flexible Scheduling**

1. **Create Events**: Plan your day with events
2. **Adapt as Needed**: Use pause/resume to handle interruptions
3. **Trust the System**: Let it handle time adjustments automatically

---

## 🔧 Advanced Features

### **Smart Auto-Reschedule**
- **30 minutes after original end time**: Events auto-reschedule
- **2 hours after pause**: Fallback safety net
- **Smart Labels**: [MISSED] vs [RESCHEDULED] events

### **Conflict Resolution**
- Automatically finds next available slot
- Preserves remaining event duration
- No manual intervention needed

### **Time Tracking**
- **[COMPLETED]** events show what you've finished
- **[MISSED]** events show what was rescheduled
- **[RESCHEDULED]** events show auto-handled pauses

---

## 🎨 UI Features

### **Responsive Design**
- Works on desktop and mobile
- Clean, modern interface
- Color-coded status indicators

### **Real-time Updates**
- Live status updates
- Instant feedback on actions
- Auto-refresh capabilities

### **Visual Analytics**
- Timeline charts
- Progress bars
- Status distributions
- Interactive data tables

### **Easy Navigation**
- Sidebar navigation
- Quick action buttons
- Expanding details sections
- Search and filter options

---

## 🛠️ Troubleshooting

### **Server Connection Issues**
- Make sure FastAPI server is running
- Check that both ports 8000 and 8501 are available
- Use `python start.py` to launch both services

### **Calendar Not Configured**
- Enter your Gmail address in the configuration
- Make sure service_account.json is valid
- Check calendar sharing permissions

### **Events Not Showing**
- Click **Refresh Events** button
- Check your calendar permissions
- Verify timezone settings

### **Pause/Resume Not Working**
- Make sure an event is currently ongoing
- Check that you have paused events to resume
- Verify server connection status

---

## 💡 Pro Tips

### **Productivity Tips**
1. **Plan Ahead**: Create events before starting work
2. **Use Pause Frequently**: Take regular breaks and use pause/resume
3. **Check Analytics**: Review your time usage patterns
4. **Trust Automation**: Let the system handle time adjustments

### **Best Practices**
1. **Consistent Naming**: Use clear event names
2. **Realistic Timing**: Set reasonable event durations
3. **Regular Reviews**: Check analytics weekly
4. **Backup Plans**: Let auto-reschedule handle conflicts

### **Power User Features**
1. **Bulk Operations**: Use force reschedule for multiple expired events
2. **Timeline View**: Visualize your entire schedule
3. **Status Tracking**: Monitor completed vs missed events
4. **Quick Actions**: Use dashboard buttons for speed

---

## 📱 Mobile Usage

The Streamlit UI works great on mobile devices:
- **Touch-friendly buttons**
- **Responsive layout**
- **Mobile navigation**
- **Quick access to pause/resume**

---

## 🔗 Integration

### **API Access**
While the UI is user-friendly, you can still use the API directly:
- **API Documentation**: http://localhost:8000/docs
- **Direct API calls**: For custom integrations
- **Webhook support**: Can be extended for notifications

### **Data Export**
- Export event data from analytics
- Download timeline charts
- Backup calendar information

---

## 🎉 Enjoy Your Smart Calendar!

The Google Calendar Pause/Resume Manager makes time management effortless:
- **No more manual time calculations**
- **Automatic conflict resolution**
- **Intelligent pause/resume functionality**
- **Beautiful analytics and insights**
- **Mobile-friendly interface**

Focus on your work/study, and let the system handle the time management! 🚀