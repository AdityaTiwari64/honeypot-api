# 🚀 Complete Submission Guide - Agentic Honey-Pot

## Current Status
✅ API code is complete
✅ Dependencies installed
✅ HONEYPOT_API_KEY set: `qay6JBQ97DhU4V2nNosA0LC5OHc3kwev`
⏳ GEMINI_API_KEY needed
⏳ Need to run and deploy API
⏳ Need to submit to GUVI

---

## Step 1: Get Gemini API Key (5 minutes)

### Option A: Using Google AI Studio (Recommended)
1. Open your browser and go to: **https://aistudio.google.com/app/apikey**
2. Sign in with your Google account
3. Click **"Get API Key"** or **"Create API Key"**
4. Select a project or create new one (it's free)
5. **Copy the key** - looks like: `AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX`

### Option B: Using Google Cloud Console
1. Go to: **https://console.cloud.google.com/**
2. Create a new project or select existing
3. Enable "Generative Language API"
4. Go to APIs & Services → Credentials
5. Create API Key
6. Copy the key

### Add to .env file
Once you have the key, edit `d:\hcl_guvi\honeypot-api\.env`:

```env
GEMINI_API_KEY=AIzaSy_paste_your_actual_key_here
```

---

## Step 2: Test API Locally (2 minutes)

### Start the server
```bash
cd d:\hcl_guvi\honeypot-api
python main.py
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### Test health check
Open a new terminal:
```bash
curl http://localhost:8000/health
```

Expected response:
```json
{
  "status": "healthy",
  "active_sessions": 0,
  "environment": "development"
}
```

### Test the honeypot endpoint
```bash
curl -X POST http://localhost:8000/api/honeypot -H "x-api-key: qay6JBQ97DhU4V2nNosA0LC5OHc3kwev" -H "Content-Type: application/json" -d @test_scam_message.json
```

You should get an AI-generated response!

---

## Step 3: Deploy Publicly (5-10 minutes)

You need a **public URL** for GUVI to test. Here are your options:

### Option A: ngrok (Fastest - Recommended for Testing)

1. **Download ngrok**: https://ngrok.com/download
2. **Extract and run**:
   ```bash
   # Make sure your API is running first (python main.py)
   # Then in a new terminal:
   ngrok http 8000
   ```
3. **Copy the public URL** shown (e.g., `https://abc123.ngrok.io`)
4. **Your API endpoint URL**: `https://abc123.ngrok.io/api/honeypot`

⚠️ **Note**: Keep both the API and ngrok running during testing/submission

### Option B: Railway (For Permanent Deployment)

1. Install Railway CLI:
   ```bash
   npm install -g @railway/cli
   ```
2. Deploy:
   ```bash
   cd d:\hcl_guvi\honeypot-api
   railway login
   railway init
   railway up
   ```
3. Add environment variables in Railway dashboard:
   - `HONEYPOT_API_KEY`: `qay6JBQ97DhU4V2nNosA0LC5OHc3kwev`
   - `GEMINI_API_KEY`: `your-gemini-key`
   - `ENVIRONMENT`: `production`
4. Get your public URL from Railway dashboard

### Option C: Render

1. Push code to GitHub
2. Go to https://render.com
3. Create new Web Service
4. Connect your repo
5. Set:
   - Build: `pip install -r requirements.txt`
   - Start: `uvicorn main:app --host 0.0.0.0 --port $PORT`
6. Add environment variables in Render dashboard
7. Deploy and get public URL

---

## Step 4: Test with GUVI Endpoint Tester

![GUVI Tester](file:///C:/Users/Aditya/.gemini/antigravity/brain/80fab643-6807-4e97-82d0-a91cc3d02b35/uploaded_media_0_1770302131647.png)

Fill in the tester:

**Headers**
- `x-api-key`: `qay6JBQ97DhU4V2nNosA0LC5OHc3kwev`

**Honeypot API Endpoint URL**
- `https://your-public-url.com/api/honeypot`
  
Example: `https://abc123.ngrok.io/api/honeypot`

Click **Test Honeypot Endpoint** and verify it works!

---

## Step 5: Submit to GUVI

![GUVI Submission](file:///C:/Users/Aditya/.gemini/antigravity/brain/80fab643-6807-4e97-82d0-a91cc3d02b35/uploaded_media_1_1770302131647.png)

Fill in the submission form:

**Deployed URL**
- `https://your-public-url.com/api/honeypot`

**API KEY**
- `qay6JBQ97DhU4V2nNosA0LC5OHc3kwev`

Click **Submit for review**

---

## Quick Reference Card

| Item | Value |
|------|-------|
| Your API Key | `qay6JBQ97DhU4V2nNosA0LC5OHc3kwev` |
| Local Endpoint | `http://localhost:8000/api/honeypot` |
| Public Endpoint | `https://your-deployed-url/api/honeypot` |
| Gemini Key | Get from: https://aistudio.google.com/app/apikey |

---

## Troubleshooting

### "GEMINI_API_KEY is required"
→ Edit `.env` file and add your Gemini API key

### "Invalid API key" when testing
→ Use `qay6JBQ97DhU4V2nNosA0LC5OHc3kwev` as the x-api-key header

### ngrok session expired
→ Free ngrok tunnels expire after 2 hours. Just restart ngrok to get a new URL

### GUVI can't reach your endpoint
→ Make sure both your API (`python main.py`) and ngrok are running
→ Test locally first before deploying

---

## Next Actions Checklist

- [ ] Get Gemini API key from https://aistudio.google.com/app/apikey
- [ ] Add Gemini key to `.env` file
- [ ] Run API locally: `python main.py`
- [ ] Test locally with curl
- [ ] Deploy publicly (ngrok recommended)
- [ ] Test with GUVI Endpoint Tester
- [ ] Submit final URL and API key to GUVI

---

## Need Help?

If you get stuck on any step, let me know which step and I'll help you troubleshoot!

Good luck! 🚀
