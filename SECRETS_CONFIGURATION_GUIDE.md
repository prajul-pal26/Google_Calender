# 🔐 Streamlit Secrets Configuration Guide

## 📋 **Step-by-Step Guide to Configure Secrets**

### **🎯 What You Need**
- Your service account JSON file (from Google Cloud Console)
- Access to your Streamlit Cloud app dashboard

---

## 🌐 **Step 1: Access Streamlit Cloud Secrets**

### **1.1 Go to Your App Dashboard**
1. Open [Streamlit Cloud](https://share.streamlit.io/)
2. Click on your deployed app
3. You'll see your app dashboard

### **1.2 Navigate to Secrets**
1. Click on **"Settings"** tab (top navigation)
2. Click on **"Secrets"** section (left sidebar)
3. You'll see a text area for secrets

---

## 🔑 **Step 2: Get Your Service Account JSON**

### **2.1 Locate Your JSON File**
Find the service account JSON file you downloaded from Google Cloud Console. It looks like this:

```json
{
  "type": "service_account",
  "project_id": "your-project-id-12345",
  "private_key_id": "key-id-abcdef123456",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQC7VJTUt9Us8cKB\n...your-private-key-here...\n-----END PRIVATE KEY-----\n",
  "client_email": "your-service-account@your-project-id.iam.gserviceaccount.com",
  "client_id": "123456789012345678901",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/your-service-account%40your-project-id.iam.gserviceaccount.com"
}
```

### **2.2 Copy the Entire JSON**
- Open the JSON file in a text editor
- Select **ALL** content (Ctrl+A or Cmd+A)
- Copy it (Ctrl+C or Cmd+C)

---

## ⚙️ **Step 3: Add Secrets to Streamlit Cloud**

### **3.1 Add Service Account Secret**
In the Secrets text area, add this:

```
service_account_json
```

**Then paste your entire JSON content as the value:**

```
service_account_json = {
  "type": "service_account",
  "project_id": "your-project-id-12345",
  "private_key_id": "key-id-abcdef123456",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQC7VJTUt9Us8cKB\n...your-private-key-here...\n-----END PRIVATE KEY-----\n",
  "client_email": "your-service-account@your-project-id.iam.gserviceaccount.com",
  "client_id": "123456789012345678901",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/your-service-account%40your-project-id.iam.gserviceaccount.com"
}
```

### **3.2 Add Timezone Secret (Optional)**
Below the service account, add:

```
DEFAULT_TIMEZONE = "Asia/Kolkata"
```

**Your complete secrets should look like:**
```
service_account_json = {
  "type": "service_account",
  "project_id": "your-project-id-12345",
  "private_key_id": "key-id-abcdef123456",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQC7VJTUt9Us8cKB\n...your-private-key-here...\n-----END PRIVATE KEY-----\n",
  "client_email": "your-service-account@your-project-id.iam.gserviceaccount.com",
  "client_id": "123456789012345678901",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/your-service-account%40your-project-id.iam.gserviceaccount.com"
}

DEFAULT_TIMEZONE = "Asia/Kolkata"
```

### **3.3 Save Secrets**
1. Click **"Save"** button at the bottom
2. Wait for the confirmation message
3. Your app will automatically restart with new secrets

---

## ✅ **Step 4: Verify Configuration**

### **4.1 Check Your App**
1. Open your app URL
2. Look at the sidebar
3. You should see: **"✅ Service account configured via Streamlit secrets"**

### **4.2 Test Connection**
1. Enter your Gmail address in the configuration
2. Click **"Configure Calendar"**
3. Should see success message

---

## 🔧 **Common Issues & Solutions**

### **Issue 1: Invalid JSON Format**
**Error:** "Failed to connect to Google Calendar"
**Solution:** 
- Make sure JSON is properly formatted
- Check all quotes and commas
- Ensure no extra characters at the end

### **Issue 2: Missing Private Key**
**Error:** Authentication fails
**Solution:**
- Verify the `private_key` field includes the complete key
- Check that `-----BEGIN PRIVATE KEY-----` and `-----END PRIVATE KEY-----` are included
- Ensure `\n` characters are preserved

### **Issue 3: Wrong Email Format**
**Error:** Calendar access denied
**Solution:**
- Verify `client_email` matches your service account email
- Ensure calendar is shared with this email address
- Check that email has "Make changes to events" permission

### **Issue 4: Secrets Not Loading**
**Error:** "Service account secrets not configured"
**Solution:**
- Verify secret name is exactly `service_account_json`
- Check that secrets were saved properly
- Try restarting your app

---

## 🎯 **Quick Validation Checklist**

- [ ] Service account JSON copied completely
- [ ] JSON format is valid (no syntax errors)
- [ ] Secret name is exactly `service_account_json`
- [ ] Private key includes BEGIN/END markers
- [ ] Client email matches your service account
- [ ] Calendar shared with service account email
- [ ] Secrets saved in Streamlit Cloud
- [ ] App shows "Service account configured" message

---

## 📱 **Visual Guide**

### **Streamlit Cloud Secrets Interface**
```
┌─────────────────────────────────────┐
│           Secrets                   │
├─────────────────────────────────────┤
│                                     │
│  [Text area for secrets]            │
│  service_account_json = {           │
│    "type": "service_account",       │
│    ...                              │
│  }                                  │
│                                     │
│  DEFAULT_TIMEZONE = "Asia/Kolkata"  │
│                                     │
│                                     │
├─────────────────────────────────────┤
│        [Save] [Cancel]              │
└─────────────────────────────────────┘
```

---

## 🚀 **You're Ready!**

Once you've completed these steps:
1. ✅ Your app will authenticate automatically
2. ✅ No more file-based authentication needed
3. ✅ Your credentials are secure in Streamlit Cloud
4. ✅ Your app is ready for production use

**🎉 Your Google Calendar Pause/Resume Manager is now fully configured!**

---

## 📞 **Need Help?**

If you encounter issues:
1. Double-check your JSON format
2. Verify calendar sharing settings
3. Check Streamlit Cloud app logs
4. Ensure all required fields are present

**Remember:** Never commit your service account JSON to git - always use Streamlit secrets!