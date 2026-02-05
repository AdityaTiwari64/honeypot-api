@echo off
REM Test script for Honeypot API

echo Testing Honeypot API...
echo.

REM Check if .env file exists
if not exist .env (
    echo ERROR: .env file not found!
    echo Please copy .env.template to .env and fill in your API keys.
    exit /b 1
)

echo 1. Testing health check...
curl -s http://localhost:8000/health
echo.
echo.

echo 2. Testing first scam message...
curl -X POST http://localhost:8000/api/honeypot ^
  -H "x-api-key: %HONEYPOT_API_KEY%" ^
  -H "Content-Type: application/json" ^
  -d @test_scam_message.json
echo.
echo.

echo 3. Testing follow-up message...
timeout /t 2 /nobreak > nul
curl -X POST http://localhost:8000/api/honeypot ^
  -H "x-api-key: %HONEYPOT_API_KEY%" ^
  -H "Content-Type: application/json" ^
  -d @test_followup_message.json
echo.
echo.

echo Testing complete!
