# 📅 Google Calendar Pause/Resume Manager

A comprehensive Google Calendar management system with intelligent automatic pause/resume functionality, deployed as a single Streamlit application.

## 🚀 Quick Start

### **Streamlit Cloud Deployment (Easiest)**

1. **Fork this repository**
2. **Go to [Streamlit Cloud](https://share.streamlit.io/)**
3. **Connect your GitHub account**
4. **Select this repository**
5. **Deploy!**

That's it! Your app will be live at `https://your-app.streamlit.app`

### **Local Development**

```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run streamlit_app.py
```

## 🎯 Features

### **Smart Pause/Resume**
- **⏸️ One-Click Pause** - Pause current ongoing event instantly
- **▶️ One-Click Resume** - Resume last paused event automatically
- **🤖 Intelligent Time Management** - Automatically extends events for breaks
- **🔄 Conflict Resolution** - Finds next available slot when needed

### **Beautiful Interface**
- **📊 Real-time Dashboard** - Live status updates
- **📈 Event Management** - Create, view, delete events
- **🎨 Modern Design** - Gradient cards and smooth animations
- **📱 Mobile Responsive** - Works on all devices

### **Advanced Features**
- **⏰ Auto-Reschedule** - Handles forgotten paused events
- **🏷️ Smart Labels** - [COMPLETED], [MISSED], [RESCHEDULED]
- **📊 Analytics** - Track your time usage patterns
- **🔐 Secure** - Uses Google service account authentication

## 📋 Setup

### **1. Google Calendar Setup**

1. **Go to [Google Cloud Console](https://console.cloud.google.com/)**
2. **Create a new project**
3. **Enable Google Calendar API**
4. **Create Service Account**
5. **Download service account JSON file**
6. **Rename it to `service_account.json`**
7. **Share your Google Calendar with the service account email**

### **2. Environment Variables (Optional)**

Create a `.env` file:
```bash
SERVICE_ACCOUNT_FILE=service_account.json
SCOPES=https://www.googleapis.com/auth/calendar
DEFAULT_TIMEZONE=Asia/Kolkata
```

### **3. Deploy to Streamlit Cloud**

1. **Upload `service_account.json` to your app secrets**
2. **Set environment variables in Streamlit Cloud**
3. **Deploy your app**

## 🎮 Daily Use

### **For Study Sessions**
1. **Create** your study events in advance
2. **Pause** when you need a break (⏸️ button)
3. **Resume** when you're back (▶️ button)
4. **System** automatically adjusts your study time

### **For Work Meetings**
1. **Schedule** your meetings
2. **Use pause/resume** as needed during meetings
3. **Let the system** handle time adjustments

### **For Flexible Scheduling**
1. **Plan** your day with events
2. **Adapt** using pause/resume for interruptions
3. **Trust** the automatic time management

## 🛠️ Technical Details

### **Architecture**
- **Single File Application** - Everything in `streamlit_app.py`
- **Google Calendar API** - Direct integration
- **In-Memory Storage** - Fast and responsive
- **No External Dependencies** - Self-contained

### **Key Functions**
- `pause_current_event()` - Pauses ongoing event
- `resume_last_event()` - Resumes paused event
- `auto_reschedule_abandoned_events()` - Handles forgotten pauses
- `find_available_slot()` - Conflict resolution
- `create_new_event()` - Event creation
- `get_all_events()` - Event listing

### **Smart Features**
- **30-minute auto-reschedule** after original end time
- **2-hour fallback** for very long pauses
- **Time zone handling** - Global compatibility
- **Error handling** - User-friendly messages

## 🔧 Configuration

### **Service Account Setup**
1. **Enable Google Calendar API** in Google Cloud Console
2. **Create Service Account** with Calendar permissions
3. **Download JSON credentials**
4. **Share calendar** with service account email
5. **Upload to Streamlit secrets**

### **Streamlit Secrets**
```toml
# In Streamlit Cloud > Settings > Secrets
SERVICE_ACCOUNT_FILE = "your-service-account-content"
SCOPES = "https://www.googleapis.com/auth/calendar"
DEFAULT_TIMEZONE = "Asia/Kolkata"
```

## 📱 Mobile Usage

The app works perfectly on mobile:
- **Touch-friendly buttons**
- **Responsive layout**
- **Mobile navigation**
- **Quick access to pause/resume**

## 🎨 UI Features

- **Gradient Cards** - Beautiful status indicators
- **Real-time Updates** - Live feedback
- **Progress Indicators** - Visual time tracking
- **Expandable Sections** - Detailed information
- **Smooth Animations** - Modern interactions

## 🔍 Troubleshooting

### **Common Issues**

1. **"Calendar not configured"**
   - Enter your Gmail address in the sidebar
   - Make sure service account has access

2. **"Failed to connect to Google Calendar"**
   - Check service account file
   - Verify API is enabled
   - Check calendar sharing permissions

3. **"No ongoing event found"**
   - Make sure you have events scheduled
   - Check event timing
   - Verify timezone settings

### **Debug Mode**
Add this to your app for debugging:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 🚀 Deployment Options

### **Streamlit Cloud (Recommended)**
- **Easiest deployment**
- **Free tier available**
- **Automatic HTTPS**
- **Built-in secrets management**

### **Other Platforms**
- **Heroku**
- **Railway**
- **PythonAnywhere**
- **Your own server**

## 📞 Support

For issues:
1. **Check the troubleshooting section**
2. **Verify your Google Calendar setup**
3. **Ensure service account permissions**
4. **Test with a simple event first**

## 🎉 Enjoy!

Focus on your work and study while the system handles all the time management complexity automatically! 🚀

---

**Made with ❤️ using Streamlit and Google Calendar API**