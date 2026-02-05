# Quick Start Guide - Agentic Honey-Pot API

## Prerequisites

Before you begin, ensure you have:
- Python 3.8+ installed
- pip (Python package manager)
- A Google Gemini API key

## Getting Your API Keys

### 1. Google Gemini API Key

1. Visit https://makersuite.google.com/app/apikey
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the generated key

### 2. Create Your Honeypot API Key

Generate a secure random key for your API:

**Option 1 - Using PowerShell:**
```powershell
-join ((65..90) + (97..122) + (48..57) | Get-Random -Count 32 | ForEach-Object {[char]$_})
```

**Option 2 - Simple String:**
```
Use any secure random string, e.g., "my-super-secret-honeypot-key-2026"
```

## Installation Steps

### Step 1: Navigate to Project Directory

```bash
cd d:\hcl_guvi\honeypot-api
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- FastAPI (Web framework)
- Uvicorn (ASGI server)
- Pydantic (Data validation)
- Google Generative AI (Gemini)
- Python-dotenv (Environment variables)
- Requests (HTTP library)

### Step 3: Create Environment File

```bash
copy .env.template .env
```

### Step 4: Edit .env File

Open `.env` in a text editor and fill in your keys:

```env
HONEYPOT_API_KEY=your-generated-honeypot-api-key-here
GEMINI_API_KEY=your-gemini-api-key-from-google
ENVIRONMENT=development
```

**Important:** Replace the placeholder values with your actual keys!

### Step 5: Run the API

```bash
python main.py
```

Or using uvicorn:

```bash
uvicorn main:app --reload
```

You should see:
```
INFO:     Started server process [xxxxx]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### Step 6: Test the API

**Test Health Check:**
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

**Test Honeypot Endpoint:**
```bash
curl -X POST http://localhost:8000/api/honeypot -H "x-api-key: your-honeypot-api-key" -H "Content-Type: application/json" -d @test_scam_message.json
```

Expected response:
```json
{
  "status": "success",
  "reply": "Why is my account being blocked?"
}
```

## Make Your API Public

### Option 1: Using ngrok (Recommended for Testing)

1. Download ngrok from https://ngrok.com/download
2. Install and authenticate
3. Run:
   ```bash
   ngrok http 8000
   ```
4. Copy the public URL (e.g., `https://abc123.ngrok.io`)
5. Use this URL for GUVI submission: `https://abc123.ngrok.io/api/honeypot`

### Option 2: Deploy to Railway

1. Install Railway CLI: `npm install -g @railway/cli`
2. Login: `railway login`
3. Initialize: `railway init`
4. Deploy: `railway up`
5. Add environment variables in Railway dashboard
6. Get your public URL

### Option 3: Deploy to Render

1. Create account at https://render.com
2. Connect your GitHub repository
3. Create new Web Service
4. Set build command: `pip install -r requirements.txt`
5. Set start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
6. Add environment variables
7. Deploy and get your public URL

## Troubleshooting

### Issue: "ModuleNotFoundError"
**Solution:** Make sure you installed all dependencies: `pip install -r requirements.txt`

### Issue: "HONEYPOT_API_KEY is required"
**Solution:** Check that `.env` file exists and contains valid keys

### Issue: "Invalid API key" when testing
**Solution:** Make sure you're using the same key in `.env` and in your curl command

### Issue: Gemini API error
**Solution:** Verify your Gemini API key is valid and has quota available

### Issue: "Address already in use"
**Solution:** Another service is using port 8000. Either stop it or use a different port:
```bash
uvicorn main:app --port 8001
```

## Next Steps

1. **Test the endpoint** using the GUVI Endpoint Tester
2. **Submit your endpoint URL** to the GUVI platform
3. **Provide your API key** for evaluation
4. **Monitor logs** to see the agent in action

## Monitoring Your API

Watch real-time logs to see scam detection and agent responses:

```bash
# In the terminal where you ran 'python main.py', you'll see:
INFO: Received message for session test-session-001
INFO: Scam detection - Session test-session-001: True (confidence: 0.85)
INFO: Scam confirmed for session test-session-001
INFO: Successfully sent callback for session test-session-001
```

## Important Notes

- **Keep your API running** during evaluation
- **Don't share your API keys** publicly
- **Monitor your Gemini API quota** to avoid exhaustion
- **Test thoroughly** before final submission

## Support

For issues or questions:
1. Check the main README.md
2. Review the implementation_plan.md
3. Check API logs for error messages

Good luck with the hackathon! 🚀
