from pydantic import BaseModel, Field
from typing import List, Optional, Dict

class Message(BaseModel):
    """Individual message in the conversation"""
    sender: str = Field(..., description="Either 'scammer' or 'user'")
    text: str = Field(..., description="Message content")
    timestamp: int = Field(..., description="Epoch time in milliseconds")

class Metadata(BaseModel):
    """Optional metadata about the conversation"""
    channel: Optional[str] = Field(None, description="SMS, WhatsApp, Email, Chat")
    language: Optional[str] = Field(None, description="Language used")
    locale: Optional[str] = Field(None, description="Country or region")

class ScamRequest(BaseModel):
    """Incoming request to the honeypot API"""
    sessionId: str = Field(..., description="Unique session identifier")
    message: Message = Field(..., description="Latest incoming message")
    conversationHistory: List[Message] = Field(default_factory=list, description="Previous messages")
    metadata: Optional[Metadata] = Field(None, description="Additional context")

class ScamResponse(BaseModel):
    """Response from the honeypot API"""
    status: str = Field(..., description="success or error")
    reply: str = Field(..., description="Agent's response to the scammer")

class IntelligenceData(BaseModel):
    """Extracted intelligence from scam conversation"""
    bankAccounts: List[str] = Field(default_factory=list)
    upiIds: List[str] = Field(default_factory=list)
    phishingLinks: List[str] = Field(default_factory=list)
    phoneNumbers: List[str] = Field(default_factory=list)
    suspiciousKeywords: List[str] = Field(default_factory=list)

class FinalResultPayload(BaseModel):
    """Payload sent to GUVI evaluation endpoint"""
    sessionId: str
    scamDetected: bool
    totalMessagesExchanged: int
    extractedIntelligence: Dict
    agentNotes: str
