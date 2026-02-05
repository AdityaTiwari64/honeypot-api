import re
from typing import Tuple

class ScamDetector:
    """Detects scam intent in messages"""
    
    # Scam indicators with weights
    URGENCY_PHRASES = [
        "urgent", "immediately", "now", "today", "expire", "suspend",
        "blocked", "locked", "verify", "confirm", "update required"
    ]
    
    FINANCIAL_THREATS = [
        "bank account", "account blocked", "account suspended", "fraud detected",
        "unauthorized transaction", "verify account", "security alert",
        "suspicious activity", "account deactivated"
    ]
    
    SENSITIVE_DATA_REQUESTS = [
        "upi", "pin", "otp", "password", "cvv", "card number", "account number",
        "aadhaar", "pan", "debit card", "credit card", "net banking",
        "atm pin", "security code"
    ]
    
    IMPERSONATION_KEYWORDS = [
        "rbi", "reserve bank", "income tax", "government", "police",
        "cyber crime", "tax department", "customs", "enforcement"
    ]
    
    REWARD_SCAMS = [
        "won", "prize", "lottery", "reward", "cashback", "refund",
        "gift", "offer", "claim", "free", "congratulations"
    ]
    
    def detect_scam(self, message_text: str, conversation_history: list = None) -> Tuple[bool, float, str]:
        """
        Detect if a message is a scam
        
        Returns:
            Tuple of (is_scam: bool, confidence: float, reason: str)
        """
        text_lower = message_text.lower()
        confidence = 0.0
        reasons = []
        
        # Check urgency phrases
        urgency_count = sum(1 for phrase in self.URGENCY_PHRASES if phrase in text_lower)
        if urgency_count > 0:
            confidence += min(urgency_count * 0.15, 0.3)
            reasons.append(f"urgency tactics ({urgency_count} indicators)")
        
        # Check financial threats
        threat_count = sum(1 for phrase in self.FINANCIAL_THREATS if phrase in text_lower)
        if threat_count > 0:
            confidence += min(threat_count * 0.2, 0.35)
            reasons.append(f"financial threats ({threat_count} indicators)")
        
        # Check sensitive data requests
        data_request_count = sum(1 for phrase in self.SENSITIVE_DATA_REQUESTS if phrase in text_lower)
        if data_request_count > 0:
            confidence += min(data_request_count * 0.25, 0.4)
            reasons.append(f"sensitive data requests ({data_request_count} indicators)")
        
        # Check impersonation
        impersonation_count = sum(1 for phrase in self.IMPERSONATION_KEYWORDS if phrase in text_lower)
        if impersonation_count > 0:
            confidence += min(impersonation_count * 0.2, 0.3)
            reasons.append(f"impersonation ({impersonation_count} indicators)")
        
        # Check reward scams
        reward_count = sum(1 for phrase in self.REWARD_SCAMS if phrase in text_lower)
        if reward_count > 0:
            confidence += min(reward_count * 0.15, 0.25)
            reasons.append(f"reward/prize tactics ({reward_count} indicators)")
        
        # Check for URLs (potential phishing)
        urls = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', text_lower)
        if urls:
            confidence += 0.2
            reasons.append(f"suspicious links ({len(urls)} found)")
        
        # Cap confidence at 1.0
        confidence = min(confidence, 1.0)
        
        # Determine if it's a scam based on threshold
        from config import config
        is_scam = confidence >= config.SCAM_CONFIDENCE_THRESHOLD
        
        reason = "; ".join(reasons) if reasons else "no scam indicators detected"
        
        return is_scam, confidence, reason
