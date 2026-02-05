# 🚀 Quick Deployment Checklist

## ✅ What's Ready
- [x] All code files created
- [x] Dependencies listed in requirements.txt
- [x] Vercel configuration (vercel.json)
- [x] Git repository initialized
- [x] Initial commit made
- [x] API key generated: `qay6JBQ97DhU4V2nNosA0LC5OHc3kwev`
- [x] Gemini API key obtained

## 📦 Deploy to Vercel - 3 Easy Steps

### Step 1: Push to GitHub (5 minutes)

1. Create a new repository on GitHub:
   - Go to https://github.com/new
   - Repository name: `honeypot-api`
   - Make it **Private** (recommended)
   - Don't initialize with README
   - Click "Create repository"

2. Push your code:
   ```bash
   cd d:\hcl_guvi\honeypot-api
   git remote add origin https://github.com/YOUR_USERNAME/honeypot-api.git
   git branch -M main
   git push -u origin main
   ```

### Step 2: Deploy on Vercel (3 minutes)

1. Go to https://vercel.com/new
2. Click "Import Git Repository"
3. Select your `honeypot-api` repository
4. **ADD ENVIRONMENT VARIABLES** (CRITICAL):
   - Click "Environment Variables"
   - Add these 3 variables:
     ```
     HONEYPOT_API_KEY = qay6JBQ97DhU4V2nNosA0LC5OHc3kwev
     GEMINI_API_KEY = [paste your Gemini key]
     ENVIRONMENT = production
     ```
5. Click **Deploy**

### Step 3: Get Your URL & Submit (2 minutes)

After deployment completes:
1. Copy your URL: `https://honeypot-api-xxxxx.vercel.app`
2. Your API endpoint: `https://honeypot-api-xxxxx.vercel.app/api/honeypot`

**Submit to GUVI:**
- **Deployed URL**: `https://honeypot-api-xxxxx.vercel.app/api/honeypot`
- **API KEY**: `qay6JBQ97DhU4V2nNosA0LC5OHc3kwev`

## 🧪 Test Before Submitting

```bash
# Test health
curl https://honeypot-api-xxxxx.vercel.app/health

# Test honeypot
curl -X POST https://honeypot-api-xxxxx.vercel.app/api/honeypot \
  -H "x-api-key: qay6JBQ97DhU4V2nNosA0LC5OHc3kwev" \
  -H "Content-Type: application/json" \
  -d "{\"sessionId\":\"test-123\",\"message\":{\"sender\":\"scammer\",\"text\":\"Your bank account will be blocked.\",\"timestamp\":1770005528731},\"conversationHistory\":[],\"metadata\":{\"channel\":\"SMS\",\"language\":\"English\",\"locale\":\"IN\"}}"
```

## 📝 Your Submission Details

**For GUVI Submission Form:**

| Field | Value |
|-------|-------|
| Deployed URL | `https://YOUR-APP.vercel.app/api/honeypot` |
| API KEY | `qay6JBQ97DhU4V2nNosA0LC5OHc3kwev` |

## ⚠️ Alternative: Use Railway (If Vercel Has Issues)

If Vercel gives problems (common with Python), use Railway instead:

```bash
npm install -g @railway/cli
cd d:\hcl_guvi\honeypot-api
railway login
railway init
railway up
```

Then add env variables in Railway dashboard. Railway is often better for FastAPI!

---

**You're all set! Good luck with your submission! 🎉**
