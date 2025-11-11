# 🔐 Environment Variables & Streamlit Secrets Setup Guide

## 📋 **Overview**

This guide shows how to set up your Google Calendar Pause/Resume Manager using **environment variables** for local development and **Streamlit secrets** for production - the most secure approach!

## 🏗️ **Authentication Priority**

The app uses this priority order:
1. **Streamlit Secrets** (Production - Highest Priority)
2. **Environment Variables** (Local Development)
3. **Service Account File** (Legacy Support)

---

## 🧪 **Local Development Setup**

### **Step 1: Create .env File**
Your `.env` file is already created with all necessary variables:

```bash
# Google Calendar Service Account Configuration
GOOGLE_SERVICE_TYPE=service_account
GOOGLE_PROJECT_ID=big-elysium-418418
GOOGLE_PRIVATE_KEY_ID=66cdf2b0222cd2f9ebdd4c62b70418e1c1458ccb
GOOGLE_PRIVATE_KEY="-----BEGIN PRIVATE KEY-----\n..."
GOOGLE_CLIENT_EMAIL=pranjul@big-elysium-418418.iam.gserviceaccount.com
GOOGLE_CLIENT_ID=108402610784667505703
GOOGLE_AUTH_URI=https://accounts.google.com/o/oauth2/auth
GOOGLE_TOKEN_URI=https://oauth2.googleapis.com/token
GOOGLE_AUTH_PROVIDER_X509_CERT_URL=https://www.googleapis.com/oauth2/v1/certs
GOOGLE_CLIENT_X509_CERT_URL=https://www.googleapis.com/robot/v1/metadata/x509/pranjul%40big-elysium-418418.iam.gserviceaccount.com
GOOGLE_UNIVERSE_DOMAIN=googleapis.com
DEFAULT_TIMEZONE=Asia/Kolkata
```

### **Step 2: Install Dependencies**
```bash
pip install -r requirements.txt
```

### **Step 3: Run Locally**
```bash
streamlit run streamlit_app.py
```

The app will automatically:
- Load environment variables from `.env`
- Show "Environment Variables" as authentication method
- Connect to Google Calendar securely

---

## 🚀 **Streamlit Cloud Production Setup**

### **Step 1: Access Streamlit Secrets**
1. Go to your Streamlit Cloud app
2. Click **Settings** → **Secrets**

### **Step 2: Add Individual Secrets**
Add each environment variable as a separate secret:

```
GOOGLE_SERVICE_TYPE = "service_account"
GOOGLE_PROJECT_ID = "big-elysium-418418"
GOOGLE_PRIVATE_KEY_ID = "66cdf2b0222cd2f9ebdd4c62b70418e1c1458ccb"
GOOGLE_PRIVATE_KEY = "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDXCJ4ZhPj8W8G8\n9IW43wQwgbncnBKiZ2l7h0rbjzbvlyZ2XmYaNTvNc6qnInqwsjRkeyZ06yJ3gHVc\nMKaTaxNs6otTJDkYjvsGq+ymubrR9d3XvgBF7oSIRKuxmRdtumEo/bp5eEhL7Oaw\nBn4n924dKWHh72NVn07M1BmF6mvt6CrfesaqZfIjW7hq/FA/bnU+fHbWDJkUCAWL\nCOA+QbE6ceLqLMtEk2hfLQjrn0QW5dhaJ9gNNk6fcq42yPgE0tLolp0uyvVxp2hw\ng9XIhx4NLdnMu9pvKCdGjhD6zIQICnXNdlBsyJlmWB/yT18mIHVWDrXppAhadJ/p\nlIoGVTDnAgMBAAECggEAAQaAaEddbCzu+xdQ58TBTrNWJAJq/rYSVxIeLUH/HwcP\nlCOCUoPQdHfmrYd3KDsqlbKGAVX6kMF+JihGN8YsfO3UiYnO5VI0FOxG6KR3Fwjr\nuLr9fnhiVLFCP9zdktq4RDklpYSv7etMIXX6JdrxhjO10O6j8n0b9wQI9K2klS1K\nElHAk489gU0EikHzA3sqbZM/OPdQp64t6sLfY7OCubzagc+8vSDAnpm3SHTUskMG\ncSyGU1lgwGK4QFLiiXnx4+O9NvrW7reGqFHVr0lw4Wm6x6YvitY+6wKnx3yVUKP0\nUB4KCCjeF+eweiL/qMAzJt6DAe51pl2cNc9gWmuRRQKBgQD+R60cnWZ5GogiUZpA\nrm0T3gSHmQ4ZrT1d1Qy+cH0PN4F5j4uT0me1HqK7N/x1/4/f3jfRMqD7x+ITrtee\nQHlr12k7B+EtOPTvUhMVcr3uBj9vu6eKGru5zvtIfk3T+hoFRpH/CLFszKbR/E6H\ntRnw1/g4M7NBTBlRm4/IdTdmnQKBgQDYfPsBQbyek/yaYQQhKEd+KyhqEUmz2dSc\n/lPhLefvqRyJXhin0EiahlsBOrKCsRJXDq9nmS7XATdJqk6xVea0y5EATeOlLc8d\n1MZKkBBygUrSO0z6WFrXR55VKuz7QoCVp8eBcquz5VFRqoYnjb8aXjVN0SLf5227\nukwwLvDcUwKBgQCTpMCiXc5TQRGMg79CEUVqhL4yka87P3jjU8JbjWs/+6WlFLEh\nusjWxJwOgvqG9UXv4dKdGH2a1Duz3BB8Zcla0a/bQ77+iBTIJOrJyF75pw0MbnRg\nXxdjUwha1mOQUqbrK0e4Qq7qkoXGZW6fo4sVagFJeNN7dZk55k59QXpSjQKBgQCL\n0LvzZddBu2XK9plKKM9zhsAFMMEe7LJJ6l+V8KX4vIl3llPqHbSmR9uCgbxEd8PW\ngd960w3TQi/I3bsRAN+NKGOvhJ5fUaSQKZkfEsfsi+AcwrvGe0W//7scWirPY3XU\nMZXB3qNR/ep1CeK2rO8dQna+mTEi1j6inYETJV3djQKBgGx45PQC+D7ek0x4fRZA\n3cMexSs/DqfaCUD6OnDxL5Y9cnw5VCyY8ryIUKbfzoa+IXbuO4WcUSXZKXb89AjF\nCFZmUbCwJcv4o/1ZTUYqterSdt0QmE69HYtRYGg9bNu0lV+10ACd52ioebrz9qjh\nMLtsWlGMEUQ8AXggD0AXBPhx\n-----END PRIVATE KEY-----\n"
GOOGLE_CLIENT_EMAIL = "pranjul@big-elysium-418418.iam.gserviceaccount.com"
GOOGLE_CLIENT_ID = "108402610784667505703"
GOOGLE_AUTH_URI = "https://accounts.google.com/o/oauth2/auth"
GOOGLE_TOKEN_URI = "https://oauth2.googleapis.com/token"
GOOGLE_AUTH_PROVIDER_X509_CERT_URL = "https://www.googleapis.com/oauth2/v1/certs"
GOOGLE_CLIENT_X509_CERT_URL = "https://www.googleapis.com/robot/v1/metadata/x509/pranjul%40big-elysium-418418.iam.gserviceaccount.com"
GOOGLE_UNIVERSE_DOMAIN = "googleapis.com"
DEFAULT_TIMEZONE = "Asia/Kolkata"
```

### **Step 3: Save and Deploy**
1. Click **Save**
2. Deploy your app to Streamlit Cloud
3. The app will automatically use secrets

---

## 🔍 **Authentication Status**

The app sidebar shows which authentication method is active:

| Method | Status | When Used |
|--------|--------|-----------|
| **Streamlit Secrets** | ✅ Configured | Production on Streamlit Cloud |
| **Environment Variables** | ✅ Configured | Local development with .env |
| **File (Legacy)** | ✅ Configured | Old service_account.json file |
| **None** | ❌ Not configured | No authentication found |

---

## 🛡️ **Security Benefits**

### **Environment Variables Approach**
- ✅ **Secure** - Credentials not in code
- ✅ **Flexible** - Easy to change values
- ✅ **Local Development** - Works without secrets
- ✅ **Production Ready** - Maps to Streamlit secrets

### **Streamlit Secrets**
- ✅ **Encrypted** - Streamlit encrypts your secrets
- ✅ **Isolated** - Separate from code
- ✅ **Version Control** - No credentials in git
- ✅ **Production Grade** - Best for deployment

---

## 🔄 **Development Workflow**

### **Local Development**
```bash
# 1. Use .env file
cp .env.example .env
# Edit .env with your credentials

# 2. Run locally
streamlit run streamlit_app.py
```

### **Production Deployment**
```bash
# 1. Push code (no credentials)
git add .
git commit -m "Update app"
git push

# 2. Configure secrets in Streamlit Cloud
# Add each environment variable as a secret

# 3. Deploy
# Streamlit Cloud auto-deploys with secrets
```

---

## 📋 **Required Variables**

### **Core Authentication**
- `GOOGLE_SERVICE_TYPE` - Service account type
- `GOOGLE_PROJECT_ID` - Your Google Cloud project ID
- `GOOGLE_PRIVATE_KEY_ID` - Private key identifier
- `GOOGLE_PRIVATE_KEY` - The private key (most important)
- `GOOGLE_CLIENT_EMAIL` - Service account email
- `GOOGLE_CLIENT_ID` - Client ID

### **Authentication URLs**
- `GOOGLE_AUTH_URI` - OAuth authorization URL
- `GOOGLE_TOKEN_URI` - Token request URL
- `GOOGLE_AUTH_PROVIDER_X509_CERT_URL` - Certificate URL
- `GOOGLE_CLIENT_X509_CERT_URL` - Client certificate URL
- `GOOGLE_UNIVERSE_DOMAIN` - Google universe domain

### **App Configuration**
- `DEFAULT_TIMEZONE` - Your timezone (e.g., "Asia/Kolkata")

---

## 🐛 **Troubleshooting**

### **Common Issues**

| Issue | Solution |
|-------|----------|
| "No authentication method found" | Set up .env locally or secrets in production |
| "Failed to connect to Google Calendar" | Check private key format and calendar sharing |
| "Environment Variables not working" | Verify .env file format and dotenv loading |
| "Streamlit Secrets not working" | Check secret names match exactly |

### **Debug Steps**
1. Check sidebar authentication status
2. Verify all required variables are set
3. Ensure private key has correct format with `\n`
4. Confirm calendar is shared with service account email

---

## 🎯 **Best Practices**

### **Security**
- Never commit `.env` file to git
- Use different service accounts for dev/prod
- Rotate private keys regularly
- Limit service account permissions

### **Development**
- Use `.env.example` as template
- Document all required variables
- Test both local and production setups
- Keep secrets and code separate

---

## 🎉 **You're Ready!**

Your Google Calendar Pause/Resume Manager now supports:
- ✅ **Secure local development** with environment variables
- ✅ **Production deployment** with Streamlit secrets
- ✅ **Flexible authentication** with multiple methods
- ✅ **Best security practices** for credentials

**🚀 Develop locally with .env, deploy to production with secrets!**