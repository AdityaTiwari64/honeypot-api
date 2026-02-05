@echo off
echo ========================================
echo   Agentic Honey-Pot - Vercel Deployment
echo ========================================
echo.

REM Check if user has Vercel CLI
where vercel >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Vercel CLI not found!
    echo.
    echo Please install it first:
    echo   npm install -g vercel
    echo.
    echo Then run this script again.
    pause
    exit /b 1
)

echo Vercel CLI found!
echo.

echo Deploying to Vercel...
echo.
echo IMPORTANT: When prompted, answer:
echo   - Set up and deploy? YES
echo   - Which scope? [Select your account]
echo   - Link to existing project? NO
echo   - Project name? honeypot-api
echo   - Directory? ./ [Just press Enter]
echo   - Override settings? NO
echo.
pause

vercel

echo.
echo ========================================
echo   Deployment Complete!
echo ========================================
echo.
echo NEXT STEPS:
echo   1. Copy the deployment URL from above
echo   2. Add environment variables in Vercel dashboard
echo   3. Redeploy with: vercel --prod
echo.
echo Environment variables to add:
echo   HONEYPOT_API_KEY = qay6JBQ97DhU4V2nNosA0LC5OHc3kwev
echo   GEMINI_API_KEY = [Your Gemini API key]
echo   ENVIRONMENT = production
echo.
pause
