from typing import Dict, Optional
from models import IntelligenceData, Message
from datetime import datetime, timedelta

class SessionData:
    """Data structure for a conversation session"""
    
    def __init__(self, session_id: str):
        self.session_id = session_id
        self.conversation_history = []
        self.scam_detected = False
        self.scam_confidence = 0.0
        self.intelligence = IntelligenceData()
        self.message_count = 0
        self.agent_notes = []
        self.created_at = datetime.now()
        self.last_updated = datetime.now()
        self.callback_sent = False
    
    def add_message(self, message: Message):
        """Add a message to conversation history"""
        self.conversation_history.append(message)
        self.message_count += 1
        self.last_updated = datetime.now()
    
    def update_intelligence(self, intelligence: IntelligenceData):
        """Update extracted intelligence"""
        self.intelligence = intelligence
        self.last_updated = datetime.now()
    
    def add_agent_note(self, note: str):
        """Add an observation to agent notes"""
        self.agent_notes.append(note)
        self.last_updated = datetime.now()
    
    def get_consolidated_notes(self) -> str:
        """Get all agent notes as a single string"""
        return " | ".join(self.agent_notes)

class SessionManager:
    """Manages conversation sessions"""
    
    def __init__(self):
        self.sessions: Dict[str, SessionData] = {}
        self.max_session_age_hours = 24
    
    def get_session(self, session_id: str) -> SessionData:
        """Get or create a session"""
        if session_id not in self.sessions:
            self.sessions[session_id] = SessionData(session_id)
        return self.sessions[session_id]
    
    def session_exists(self, session_id: str) -> bool:
        """Check if session exists"""
        return session_id in self.sessions
    
    def update_session(self, session_id: str, session_data: SessionData):
        """Update session data"""
        self.sessions[session_id] = session_data
    
    def cleanup_old_sessions(self):
        """Remove sessions older than max age"""
        cutoff_time = datetime.now() - timedelta(hours=self.max_session_age_hours)
        sessions_to_remove = [
            session_id for session_id, session_data in self.sessions.items()
            if session_data.last_updated < cutoff_time
        ]
        
        for session_id in sessions_to_remove:
            del self.sessions[session_id]
        
        return len(sessions_to_remove)
    
    def get_session_count(self) -> int:
        """Get total number of active sessions"""
        return len(self.sessions)

# Global session manager instance
session_manager = SessionManager()
