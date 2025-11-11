# 🚀 Streamlit Cloud Setup Checklist

## ✅ **Pre-Deployment Checklist**

### **📁 Repository Setup**
- [ ] Code pushed to GitHub repository
- [ ] `streamlit_app.py` in root directory
- [ ] `requirements.txt` includes all dependencies
- [ ] No service account JSON files in repository
- [ ] `.gitignore` excludes sensitive files

### **🔑 Google Calendar Setup**
- [ ] Service account created in Google Cloud Console
- [ ] Google Calendar API enabled
- [ ] Calendar shared with service account email
- [ ] Service account has "Make changes to events" permission
- [ ] Service account JSON downloaded (keep secure!)

### **🌐 Streamlit Cloud Setup**
- [ ] Streamlit Cloud account created
- [ ] New app created from GitHub repository
- [ ] Main file path set to `streamlit_app.py`
- [ ] App deployed successfully

## 🔐 **Streamlit Secrets Configuration**

### **Required Secrets**
Add these in **Streamlit Cloud → Settings → Secrets**:

```
service_account_json
```
**Value:** Your complete service account JSON content

```
DEFAULT_TIMEZONE (optional)
```
**Value:** `Asia/Kolkata` (or your timezone)

### **Secret Format Example**
```json
{
  "type": "service_account",
  "project_id": "your-project-id",
  "private_key_id": "key-id",
  "private_key": "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n",
  "client_email": "your-service-account@your-project.iam.gserviceaccount.com",
  "client_id": "your-client-id",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/..."
}
```

## 🧪 **Post-Deployment Testing**

### **Basic Functionality**
- [ ] App loads without errors
- [ ] Sidebar shows "✅ Service account configured via Streamlit secrets"
- [ ] Calendar configuration works with Gmail address
- [ ] Dashboard displays correctly

### **Pause/Resume Testing**
- [ ] Create test event in Google Calendar
- [ ] Pause current event works
- [ ] Completed event created in past
- [ ] Resume last event works
- [ ] Event reschedules correctly

### **Edge Cases**
- [ ] No ongoing event shows appropriate error
- [ ] Multiple events handled correctly
- [ ] Timezone conversion works
- [ ] Auto-reschedule triggers after 2+ hours

## 🔧 **Troubleshooting Quick Guide**

### **Common Issues & Solutions**

| Issue | Solution |
|-------|----------|
| "Service account secrets not configured" | Add `service_account_json` in Streamlit secrets |
| "Failed to connect to Google Calendar" | Check API enabled and calendar sharing |
| "No ongoing event found" | Create event that includes current time |
| "Calendar not configured" | Enter Gmail and click configure |
| App won't load | Check requirements.txt and dependencies |

### **Debug Steps**
1. Check Streamlit Cloud app logs
2. Verify secrets are correctly formatted
3. Test service account permissions
4. Confirm calendar sharing settings

## 📊 **Monitoring Checklist**

### **Regular Checks**
- [ ] App status is healthy
- [ ] No error messages in logs
- [ ] API usage within limits
- [ ] Calendar events syncing properly

### **Performance**
- [ ] App loads quickly
- [ ] Pause/resume actions responsive
- [ ] No timeout errors
- [ ] Mobile interface works

## 🔄 **Maintenance**

### **Updates**
- [ ] Code changes pushed to GitHub
- [ ] Streamlit auto-deploys (if enabled)
- [ ] Secrets updated if needed
- [ ] Dependencies kept current

### **Security**
- [ ] Service account keys rotated regularly
- [ ] Access permissions reviewed
- [ ] No sensitive data in code
- [ ] Calendar sharing permissions minimal

## 🎯 **Success Criteria**

Your deployment is successful when:
- ✅ App loads and shows service account connected
- ✅ You can configure your calendar with Gmail
- ✅ Pause/resume functionality works end-to-end
- ✅ Events appear correctly in Google Calendar
- ✅ No authentication errors in logs

## 📞 **Help Resources**

- [Streamlit Cloud Documentation](https://docs.streamlit.io/streamlit-cloud)
- [Google Calendar API Documentation](https://developers.google.com/calendar)
- [Service Account Setup Guide](https://cloud.google.com/iam/docs/creating-managing-service-accounts)

---

**🚀 Ready to deploy? Follow this checklist step by step!**