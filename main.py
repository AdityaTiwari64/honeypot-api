from fastapi import FastAPI, HTTPException, Header, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import logging
from typing import Optional

from models import ScamRequest, ScamResponse, FinalResultPayload, Message
from config import config
from scam_detector import ScamDetector
from ai_agent import AIAgent
from intelligence_extractor import IntelligenceExtractor
from session_manager import session_manager
from callback_handler import callback_handler

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Validate configuration on startup
try:
    config.validate()
except ValueError as e:
    logger.error(f"Configuration error: {e}")
    raise

# Initialize FastAPI app
app = FastAPI(
    title="Agentic Honey-Pot API",
    description="AI-powered honeypot for scam detection and intelligence extraction",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components
scam_detector = ScamDetector()
ai_agent = AIAgent()
intelligence_extractor = IntelligenceExtractor()

# Thresholds for triggering callback
CALLBACK_MIN_MESSAGES = 3
CALLBACK_MIN_INTELLIGENCE_ITEMS = 1

def verify_api_key(x_api_key: Optional[str] = Header(None)):
    """Verify API key authentication"""
    if not x_api_key:
        raise HTTPException(status_code=401, detail="API key is required")
    
    if x_api_key != config.HONEYPOT_API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API key")
    
    return x_api_key

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "online",
        "service": "Agentic Honey-Pot API",
        "version": "1.0.0"
    }

@app.get("/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "active_sessions": session_manager.get_session_count(),
        "environment": config.ENVIRONMENT
    }

@app.post("/api/honeypot", response_model=ScamResponse)
async def honeypot_endpoint(
    request: ScamRequest,
    x_api_key: str = Header(None, alias="x-api-key")
):
    """
    Main honeypot endpoint for receiving and processing scam messages
    
    This endpoint:
    1. Detects scam intent
    2. Activates AI agent if scam detected
    3. Extracts intelligence
    4. Returns agent's response
    5. Sends callback when sufficient intelligence is gathered
    """
    # Verify authentication
    verify_api_key(x_api_key)
    
    try:
        session_id = request.sessionId
        latest_message = request.message
        conversation_history = request.conversationHistory
        
        logger.info(f"Received message for session {session_id}")
        
        # Get or create session
        session = session_manager.get_session(session_id)
        
        # Add the latest message to session
        session.add_message(latest_message)
        
        # Detect scam intent
        is_scam, confidence, reason = scam_detector.detect_scam(
            latest_message.text,
            conversation_history
        )
        
        logger.info(f"Scam detection - Session {session_id}: {is_scam} (confidence: {confidence:.2f})")
        
        # Update session scam status
        if is_scam and not session.scam_detected:
            session.scam_detected = True
            session.scam_confidence = confidence
            session.add_agent_note(f"Scam detected: {reason}")
            logger.info(f"Scam confirmed for session {session_id}")
        
        # Extract intelligence from the latest message
        session.intelligence = intelligence_extractor.extract_from_message(
            latest_message.text,
            session.intelligence
        )
        
        # Also extract from full conversation history if this is first detection
        if is_scam and len(conversation_history) > 0:
            all_messages = conversation_history + [latest_message]
            session.intelligence = intelligence_extractor.extract_from_conversation(all_messages)
        
        # Generate agent response
        if is_scam or session.scam_detected:
            # AI agent engages with the scammer
            reply = ai_agent.generate_response(
                latest_message.text,
                conversation_history,
                confidence
            )
            
            # Add agent's response to conversation
            agent_message = Message(
                sender="user",
                text=reply,
                timestamp=latest_message.timestamp + 1000
            )
            session.add_message(agent_message)
            
        else:
            # Not detected as scam yet, respond neutrally
            reply = "I'm not sure I understand. Can you explain more?"
        
        # Check if we should send callback
        should_send_callback = (
            session.scam_detected and 
            not session.callback_sent and
            session.message_count >= CALLBACK_MIN_MESSAGES and
            _has_sufficient_intelligence(session)
        )
        
        if should_send_callback:
            _send_evaluation_callback(session)
            session.callback_sent = True
        
        # Update session in manager
        session_manager.update_session(session_id, session)
        
        # Clean up old sessions periodically
        if session.message_count % 10 == 0:
            cleaned = session_manager.cleanup_old_sessions()
            if cleaned > 0:
                logger.info(f"Cleaned up {cleaned} old sessions")
        
        return ScamResponse(
            status="success",
            reply=reply
        )
    
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

def _has_sufficient_intelligence(session) -> bool:
    """Check if enough intelligence has been extracted"""
    intel = session.intelligence
    total_items = (
        len(intel.bankAccounts) +
        len(intel.upiIds) +
        len(intel.phishingLinks) +
        len(intel.phoneNumbers)
    )
    return total_items >= CALLBACK_MIN_INTELLIGENCE_ITEMS

def _send_evaluation_callback(session):
    """Send final results to GUVI evaluation endpoint"""
    try:
        payload = FinalResultPayload(
            sessionId=session.session_id,
            scamDetected=session.scam_detected,
            totalMessagesExchanged=session.message_count,
            extractedIntelligence={
                "bankAccounts": session.intelligence.bankAccounts,
                "upiIds": session.intelligence.upiIds,
                "phishingLinks": session.intelligence.phishingLinks,
                "phoneNumbers": session.intelligence.phoneNumbers,
                "suspiciousKeywords": session.intelligence.suspiciousKeywords
            },
            agentNotes=session.get_consolidated_notes()
        )
        
        success, message = callback_handler.send_final_result(payload)
        
        if success:
            logger.info(f"Callback sent successfully for session {session.session_id}")
        else:
            logger.warning(f"Callback failed for session {session.session_id}: {message}")
    
    except Exception as e:
        logger.error(f"Error sending callback: {str(e)}", exc_info=True)

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Custom HTTP exception handler"""
    return JSONResponse(
        status_code=exc.status_code,
        content={"status": "error", "detail": exc.detail}
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=config.ENVIRONMENT == "development"
    )
