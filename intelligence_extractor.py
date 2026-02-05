import re
from models import IntelligenceData

class IntelligenceExtractor:
    """Extracts intelligence from scam conversations"""
    
    def __init__(self):
        # Regex patterns for various data types
        self.bank_account_pattern = re.compile(r'\b\d{9,18}\b')
        self.upi_pattern = re.compile(r'\b[a-zA-Z0-9._-]+@[a-zA-Z0-9]+\b')
        self.url_pattern = re.compile(
            r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        )
        self.phone_pattern = re.compile(r'(?:\+91|0)?[6789]\d{9}')
        
        # Suspicious keywords to track
        self.suspicious_terms = [
            "urgent", "verify", "blocked", "suspend", "otp", "pin",
            "password", "account", "transfer", "payment", "claim",
            "prize", "reward", "refund", "cashback"
        ]
    
    def extract_from_message(self, message_text: str, intelligence: IntelligenceData) -> IntelligenceData:
        """
        Extract intelligence from a single message
        
        Args:
            message_text: The message to analyze
            intelligence: Existing intelligence data to update
            
        Returns:
            Updated intelligence data
        """
        # Extract bank accounts
        bank_accounts = self.bank_account_pattern.findall(message_text)
        for account in bank_accounts:
            if account not in intelligence.bankAccounts:
                intelligence.bankAccounts.append(account)
        
        # Extract UPI IDs
        upi_ids = self.upi_pattern.findall(message_text)
        for upi in upi_ids:
            # Filter out common email domains that aren't UPI
            if any(domain in upi.lower() for domain in ['@gmail', '@yahoo', '@hotmail', '@outlook']):
                continue
            if upi not in intelligence.upiIds:
                intelligence.upiIds.append(upi)
        
        # Extract phishing links
        urls = self.url_pattern.findall(message_text)
        for url in urls:
            if url not in intelligence.phishingLinks:
                intelligence.phishingLinks.append(url)
        
        # Extract phone numbers
        phones = self.phone_pattern.findall(message_text)
        for phone in phones:
            # Normalize phone number
            normalized = phone.replace('+91', '').replace('0', '', 1) if phone.startswith('0') else phone.replace('+91', '')
            if normalized not in intelligence.phoneNumbers:
                intelligence.phoneNumbers.append(normalized)
        
        # Extract suspicious keywords
        text_lower = message_text.lower()
        for term in self.suspicious_terms:
            if term in text_lower and term not in intelligence.suspiciousKeywords:
                intelligence.suspiciousKeywords.append(term)
        
        return intelligence
    
    def extract_from_conversation(self, messages: list) -> IntelligenceData:
        """
        Extract intelligence from entire conversation history
        
        Args:
            messages: List of message dicts with 'sender' and 'text' keys
            
        Returns:
            Consolidated intelligence data
        """
        intelligence = IntelligenceData()
        
        for msg in messages:
            if isinstance(msg, dict):
                text = msg.get('text', '')
            else:
                text = msg.text
            
            intelligence = self.extract_from_message(text, intelligence)
        
        return intelligence
