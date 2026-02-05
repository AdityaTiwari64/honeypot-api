# Agentic Honey-Pot API

AI-powered honeypot system for detecting scam messages, autonomously engaging scammers, and extracting intelligence.

## Features

- **Scam Detection**: Pattern-based detection of various scam types (bank fraud, UPI scams, phishing, etc.)
- **AI Agent**: Google Gemini-powered conversational agent that engages scammers naturally
- **Intelligence Extraction**: Automatically extracts bank accounts, UPI IDs, phone numbers, phishing links, and keywords
- **Session Management**: Tracks multi-turn conversations with automatic cleanup
- **Evaluation Callback**: Reports final results to GUVI evaluation endpoint

## Technology Stack

- **FastAPI**: Modern Python web framework
- **Google Gemini**: LLM for AI agent conversations
- **Pydantic**: Data validation and serialization
- **Uvicorn**: ASGI server

## Setup Instructions

### 1. Install Dependencies

```bash
cd honeypot-api
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Copy the environment template and fill in your keys:

```bash
copy .env.template .env
```

Edit `.env` and set:
- `HONEYPOT_API_KEY`: Your secret API key for securing the endpoint
- `GEMINI_API_KEY`: Your Google Gemini API key (get from https://makersuite.google.com/app/apikey)
- `ENVIRONMENT`: Set to `development` or `production`

### 3. Run the API

```bash
python main.py
```

Or using uvicorn directly:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

The API will be available at `http://localhost:8000`

## API Documentation

### Authentication

All requests require the `x-api-key` header:

```
x-api-key: your-secret-api-key-here
```

### Endpoints

#### Health Check
```bash
GET /
GET /health
```

#### Main Honeypot Endpoint
```bash
POST /api/honeypot
Content-Type: application/json
x-api-key: your-api-key
```

**Request Body:**
```json
{
  "sessionId": "unique-session-id",
  "message": {
    "sender": "scammer",
    "text": "Your bank account will be blocked. Verify immediately.",
    "timestamp": 1770005528731
  },
  "conversationHistory": [],
  "metadata": {
    "channel": "SMS",
    "language": "English",
    "locale": "IN"
  }
}
```

**Response:**
```json
{
  "status": "success",
  "reply": "Why is my account being blocked?"
}
```

## Testing

### Test with curl

**First Message:**
```bash
curl -X POST http://localhost:8000/api/honeypot \
  -H "x-api-key: your-secret-api-key-here" \
  -H "Content-Type: application/json" \
  -d "{\"sessionId\":\"test-123\",\"message\":{\"sender\":\"scammer\",\"text\":\"Your bank account will be blocked today. Verify immediately at http://fake-bank.com\",\"timestamp\":1770005528731},\"conversationHistory\":[],\"metadata\":{\"channel\":\"SMS\",\"language\":\"English\",\"locale\":\"IN\"}}"
```

**Follow-up Message:**
```bash
curl -X POST http://localhost:8000/api/honeypot \
  -H "x-api-key: your-secret-api-key-here" \
  -H "Content-Type: application/json" \
  -d "{\"sessionId\":\"test-123\",\"message\":{\"sender\":\"scammer\",\"text\":\"Share your UPI ID scammer@paytm to avoid suspension\",\"timestamp\":1770005528731},\"conversationHistory\":[{\"sender\":\"scammer\",\"text\":\"Your bank account will be blocked.\",\"timestamp\":1770005528731},{\"sender\":\"user\",\"text\":\"Why?\",\"timestamp\":1770005528732}],\"metadata\":{\"channel\":\"SMS\",\"language\":\"English\",\"locale\":\"IN\"}}"
```

## Deployment

### Using ngrok (for testing)

1. Run the API locally
2. Expose it via ngrok:
```bash
ngrok http 8000
```
3. Use the ngrok URL as your public endpoint

### Cloud Deployment

The API can be deployed to:
- **Railway**: `railway up`
- **Render**: Connect your GitHub repo
- **Vercel**: Add `vercel.json` configuration
- **Google Cloud Run**: Deploy as a container

## How It Works

1. **Message Reception**: API receives a message via POST request
2. **Scam Detection**: Pattern matching identifies scam indicators
3. **Session Management**: Conversation state is tracked per session
4. **AI Engagement**: If scam detected, Gemini generates natural responses
5. **Intelligence Extraction**: Regex patterns extract sensitive data
6. **Callback**: When sufficient intelligence is gathered, results are sent to GUVI endpoint

## File Structure

```
honeypot-api/
├── main.py                    # FastAPI application
├── models.py                  # Pydantic data models
├── config.py                  # Configuration management
├── scam_detector.py          # Scam detection logic
├── ai_agent.py               # AI agent with Gemini
├── intelligence_extractor.py # Data extraction
├── session_manager.py        # Session tracking
├── callback_handler.py       # GUVI callback
├── requirements.txt          # Dependencies
├── .env.template            # Environment template
├── .gitignore               # Git ignore rules
└── README.md                # This file
```

## Environment Variables Reference

| Variable | Description | Required |
|----------|-------------|----------|
| `HONEYPOT_API_KEY` | Your API key for endpoint authentication | Yes |
| `GEMINI_API_KEY` | Google Gemini API key | Yes |
| `ENVIRONMENT` | `development` or `production` | No (default: development) |

## Scam Detection Indicators

The system detects scams based on:
- Urgency phrases (urgent, immediately, expire, etc.)
- Financial threats (account blocked, fraud detected, etc.)
- Sensitive data requests (UPI, PIN, OTP, password, etc.)
- Impersonation (RBI, police, tax department, etc.)
- Reward scams (won, prize, lottery, etc.)
- Suspicious URLs

## Intelligence Extracted

- **Bank Accounts**: 9-18 digit account numbers
- **UPI IDs**: Pattern matching for name@bank format
- **Phishing Links**: All URLs in messages
- **Phone Numbers**: Indian mobile numbers (with/without +91)
- **Keywords**: Suspicious terms used in conversation

## Callback Behavior

A callback to GUVI evaluation endpoint is triggered when:
- Scam is detected
- At least 3 messages have been exchanged
- At least 1 intelligence item has been extracted
- Callback hasn't been sent yet for this session

## Troubleshooting

**API Key Error**: Ensure `.env` file exists and contains valid keys

**Gemini API Error**: Verify your Gemini API key at https://makersuite.google.com/app/apikey

**Connection Error**: Check that the API is running and accessible

**Callback Failed**: Check logs for specific error messages

## License

This project is created for the HCL GUVI Hackathon - Agentic Honey-Pot Challenge.
