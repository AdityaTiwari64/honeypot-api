# Vercel Deployment Guide for Agentic Honey-Pot API

## Prerequisites
- Vercel account (sign up at https://vercel.com)
- GitHub account
- Your code pushed to GitHub

## Step 1: Push to GitHub

If you haven't already, initialize git and push to GitHub:

```bash
cd d:\hcl_guvi\honeypot-api

# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit - Agentic Honey-Pot API"

# Create a new repository on GitHub, then:
git remote add origin https://github.com/YOUR_USERNAME/honeypot-api.git
git branch -M main
git push -u origin main
```

## Step 2: Deploy to Vercel

### Option A: Via Vercel Dashboard (Recommended)

1. **Go to Vercel**: https://vercel.com/new
2. **Import your GitHub repository**
3. **Configure Project**:
   - Framework Preset: **Other**
   - Root Directory: `./` (leave as is)
   - Build Command: (leave empty)
   - Output Directory: (leave empty)

4. **Add Environment Variables** (IMPORTANT):
   Click "Environment Variables" and add:
   
   | Name | Value |
   |------|-------|
   | `HONEYPOT_API_KEY` | `qay6JBQ97DhU4V2nNosA0LC5OHc3kwev` |
   | `GEMINI_API_KEY` | Your Gemini API key from Google |
   | `ENVIRONMENT` | `production` |

5. **Click Deploy**

### Option B: Via Vercel CLI

```bash
# Install Vercel CLI
npm install -g vercel

# Login to Vercel
vercel login

# Deploy (from your project directory)
cd d:\hcl_guvi\honeypot-api
vercel

# Follow the prompts:
# - Set up and deploy? Yes
# - Which scope? (select your account)
# - Link to existing project? No
# - Project name? honeypot-api
# - Directory? ./
# - Override settings? No
```

After deployment, add environment variables:
```bash
vercel env add HONEYPOT_API_KEY
# Paste: qay6JBQ97DhU4V2nNosA0LC5OHc3kwev

vercel env add GEMINI_API_KEY
# Paste your Gemini API key

vercel env add ENVIRONMENT
# Type: production

# Redeploy with env variables
vercel --prod
```

## Step 3: Get Your Deployment URL

After deployment, Vercel will give you a URL like:
- `https://honeypot-api-xxxxx.vercel.app`

Your API endpoint will be:
- `https://honeypot-api-xxxxx.vercel.app/api/honeypot`

## Step 4: Test Your Deployment

```bash
# Replace with your actual Vercel URL
curl https://honeypot-api-xxxxx.vercel.app/health

# Test the honeypot endpoint
curl -X POST https://honeypot-api-xxxxx.vercel.app/api/honeypot \
  -H "x-api-key: qay6JBQ97DhU4V2nNosA0LC5OHc3kwev" \
  -H "Content-Type: application/json" \
  -d @test_scam_message.json
```

## Step 5: Submit to GUVI

Use these values in the GUVI submission form:

**Deployed URL**:
```
https://honeypot-api-xxxxx.vercel.app/api/honeypot
```

**API KEY**:
```
qay6JBQ97DhU4V2nNosA0LC5OHc3kwev
```

## Important Notes

### Vercel Limitations for Python
- ⚠️ **Serverless timeout**: Free tier has 10-second execution limit
- ⚠️ **Cold starts**: First request may be slow
- ⚠️ **Memory limit**: 1GB on free tier

If you encounter issues, consider using **Railway** or **Render** instead (both have better Python support).

### Alternative: Railway (Recommended for Python)

If Vercel has issues, use Railway instead:

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login and deploy
railway login
railway init
railway up

# Add environment variables in Railway dashboard
# Get your public URL from Railway
```

Railway is often better for Python/FastAPI apps!

## Troubleshooting

### "Module not found" errors
- Make sure `requirements.txt` is in the root directory
- Vercel should auto-detect and install dependencies

### "Deployment failed"
- Check build logs in Vercel dashboard
- Ensure all dependencies are in `requirements.txt`

### "Timeout" errors
- Gemini API calls might be slow on cold starts
- Consider using Railway or Render for longer timeouts

### Environment variables not working
- Make sure you added them in Vercel dashboard
- Redeploy after adding env variables

## Quick Reference

| Item | Value |
|------|-------|
| Your API Key | `qay6JBQ97DhU4V2nNosA0LC5OHc3kwev` |
| Vercel Dashboard | https://vercel.com/dashboard |
| GitHub Repo | https://github.com/YOUR_USERNAME/honeypot-api |
| Endpoint Path | `/api/honeypot` |
| Full URL | `https://your-app.vercel.app/api/honeypot` |

---

Good luck with your deployment! 🚀
