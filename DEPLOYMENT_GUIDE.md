# 🚀 Streamlit Cloud Deployment Guide

## 📋 Overview

This guide will help you deploy your **Google Calendar Pause/Resume Manager** to Streamlit Cloud using **secrets-based authentication** for secure credential management.

## 🔑 **Step 1: Get Your Service Account JSON**

### **1.1 Create/Get Service Account**
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Select your project or create a new one
3. Navigate to **IAM & Admin** → **Service Accounts**
4. Create a new service account or use existing one
5. Download the JSON file (keep it secure!)

### **1.2 Enable Google Calendar API**
1. In Google Cloud Console, go to **APIs & Services** → **Library**
2. Search for "Google Calendar API"
3. Click **Enable**
4. Make sure it's enabled for your project

### **1.3 Share Calendar with Service Account**
1. Copy the `client_email` from your service account JSON
2. Go to [Google Calendar](https://calendar.google.com/)
3. Find the calendar you want to manage
4. Click on the three dots → **Settings and sharing**
5. Scroll to **Share with specific people**
6. Add the service account email with **"Make changes to events"** permission

## 🌐 **Step 2: Deploy to Streamlit Cloud**

### **2.1 Prepare Your Repository**
1. Make sure your code is on GitHub
2. Ensure `streamlit_app.py` is in the root directory
3. Verify `requirements.txt` includes all dependencies

### **2.2 Create Streamlit App**
1. Go to [Streamlit Cloud](https://share.streamlit.io/)
2. Click **"New app"**
3. Connect your GitHub repository
4. Select the repository and branch
5. Set main file path to `streamlit_app.py`
6. Click **"Deploy"**

## 🔐 **Step 3: Configure Streamlit Secrets**

### **3.1 Access Secrets**
1. In your Streamlit app dashboard
2. Click on your app
3. Go to **Settings** → **Secrets**

### **3.2 Add Service Account JSON**
Add this secret:

```
service_account_json
```

**Value:** Your entire service account JSON content (copy-paste the entire JSON)

**Example:**
```json
{
  "type": "service_account",
  "project_id": "your-project-id",
  "private_key_id": "key-id",
  "private_key": "-----BEGIN PRIVATE KEY-----\nYour-private-key-here\n-----END PRIVATE KEY-----\n",
  "client_email": "your-service-account@your-project.iam.gserviceaccount.com",
  "client_id": "your-client-id",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/your-service-account%40your-project.iam.gserviceaccount.com"
}
```

### **3.3 Add Timezone (Optional)**
```
DEFAULT_TIMEZONE
```
**Value:** `Asia/Kolkata` (or your preferred timezone)

## ✅ **Step 4: Verify Deployment**

### **4.1 Check App Status**
1. Wait for deployment to complete
2. Open your app URL
3. Check the sidebar for service account status

### **4.2 Test Connection**
1. Enter your Gmail address in the configuration
2. Click "Configure Calendar"
3. Should see "✅ Service account configured via Streamlit secrets"

## 🎯 **Step 5: Test Functionality**

### **5.1 Test Pause/Resume**
1. Create a test event in your Google Calendar
2. Use the app to pause the current event
3. Verify it creates a completed event and pauses correctly
4. Resume the event and verify it reschedules properly

### **5.2 Test Auto-Reschedule**
1. Pause an event and wait 2+ hours
2. Check if it auto-reschedules
3. Verify the new event appears in calendar

## 🔧 **Troubleshooting**

### **Common Issues**

#### **1. "Service account secrets not configured"**
- **Solution:** Add `service_account_json` secret in Streamlit Cloud settings
- **Check:** Make sure the JSON is complete and valid

#### **2. "Failed to connect to Google Calendar"**
- **Solution:** Verify service account has Calendar API access
- **Check:** Ensure calendar is shared with service account email

#### **3. "Calendar not configured"**
- **Solution:** Enter your Gmail address and click configure
- **Check:** Make sure you have permission to access the calendar

#### **4. "No ongoing event found"**
- **Solution:** Create an event that's currently running
- **Check:** Verify event time includes current time

### **Debug Mode**
Add this to your app for debugging:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 📊 **Monitoring**

### **App Health**
- Check Streamlit Cloud dashboard for app status
- Monitor logs for any errors
- Verify API usage in Google Cloud Console

### **Performance**
- Streamlit Cloud automatically handles scaling
- Monitor response times
- Check for any rate limiting

## 🔄 **Updates**

### **Updating Your App**
1. Push changes to GitHub
2. Streamlit Cloud auto-deploys (if enabled)
3. Or manually trigger redeploy in dashboard

### **Updating Secrets**
1. Go to Settings → Secrets
2. Update the secret values
3. Restart your app if needed

## 🛡️ **Security**

### **Best Practices**
- Never commit service account JSON to git
- Use Streamlit secrets for all sensitive data
- Regularly rotate service account keys
- Limit service account permissions

### **Access Control**
- Only share calendar with necessary permissions
- Use separate service accounts for different apps
- Monitor API usage and access logs

## 📱 **Mobile Access**

### **Responsive Design**
Your app works on mobile devices:
- Pause/resume events on the go
- View calendar status
- Manage events from anywhere

## 🎉 **Success!**

Your Google Calendar Pause/Resume Manager is now:
- ✅ **Deployed on Streamlit Cloud**
- ✅ **Using secure secrets authentication**
- ✅ **Ready for production use**
- ✅ **Accessible from anywhere**

## 📞 **Support**

If you encounter issues:
1. Check Streamlit Cloud documentation
2. Review Google Calendar API docs
3. Verify service account permissions
4. Check calendar sharing settings

---

**🚀 Your app is now live and ready to use!**