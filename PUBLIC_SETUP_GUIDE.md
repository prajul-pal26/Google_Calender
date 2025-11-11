# 🚀 Public Setup Guide - No Secrets Required

## 📋 **Overview**

This guide shows how to set up your Google Calendar Pause/Resume Manager using **public file-based configuration** - no secrets, no environment variables needed!

## 📁 **Required Files**

You only need **one file** in your app directory:

```
service_account.json
```

## 🔑 **Step 1: Get Your Service Account JSON**

### **1.1 Create Service Account**
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Select your project
3. **IAM & Admin** → **Service Accounts**
4. Create service account or use existing
5. Download the JSON file

### **1.2 Enable Google Calendar API**
1. **APIs & Services** → **Library**
2. Search "Google Calendar API"
3. Click **Enable**

### **1.3 Share Calendar**
1. Copy `client_email` from your JSON
2. Go to [Google Calendar](https://calendar.google.com/)
3. Share calendar with service account email
4. Give "Make changes to events" permission

## 📂 **Step 2: Setup Your Project**

### **2.1 File Structure**
```
your-project/
├── streamlit_app.py
├── service_account.json  ← Upload this file
├── requirements.txt
└── README.md
```

### **2.2 Upload Service Account File**
1. Copy your `service_account.json` to the project directory
2. Make sure it's in the same folder as `streamlit_app.py`

## 🚀 **Step 3: Deploy**

### **3.1 Local Development**
```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run streamlit_app.py
```

### **3.2 Streamlit Cloud Deployment**
1. Push your code to GitHub (including `service_account.json`)
2. Deploy to Streamlit Cloud
3. App will automatically find the service account file

## ✅ **Step 4: Verify Setup**

### **4.1 Check Sidebar**
Your app sidebar should show:
- ✅ **Service account file found**

### **4.2 Configure Calendar**
1. Enter your Gmail address
2. Click "Configure Calendar"
3. Should see success message

## 🔧 **How It Works**

### **File-Based Authentication**
```python
# The app automatically looks for service_account.json
if os.path.exists("service_account.json"):
    creds = Credentials.from_service_account_file("service_account.json", scopes=SCOPES)
```

### **No Secrets Needed**
- ❌ No `st.secrets` configuration
- ❌ No environment variables
- ❌ No `.env` files
- ✅ Just upload the JSON file

## 🎯 **Benefits**

- **Simple Setup** - Just upload one file
- **No Configuration** - Works out of the box
- **Easy Debugging** - File is visible and accessible
- **Quick Deployment** - No secret management needed

## ⚠️ **Security Note**

This approach is **less secure** than using secrets because:
- Service account JSON is visible in your repository
- Anyone with access to your code can see the credentials
- **Only use for development/testing or public projects**

## 🔒 **For Production**

For production use, consider:
1. **Streamlit Secrets** (recommended)
2. **Environment variables**
3. **Cloud credential management**

## 📱 **Testing**

### **Quick Test**
1. Create an event in your Google Calendar
2. Open the app
3. Click "Pause Current Event"
4. Verify it works correctly

### **Troubleshooting**
| Issue | Solution |
|-------|----------|
| "Service account file not found" | Upload `service_account.json` to app directory |
| "Failed to connect" | Check JSON format and calendar sharing |
| "Calendar not configured" | Enter Gmail and click configure |

## 🎉 **You're Ready!**

Your Google Calendar Pause/Resume Manager is now:
- ✅ **Configured with public file**
- ✅ **No secrets required**
- ✅ **Ready for deployment**
- ✅ **Simple to maintain**

**🚀 Just upload your service_account.json and start using the app!**