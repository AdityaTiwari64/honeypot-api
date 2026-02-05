import google.generativeai as genai
from typing import List
from models import Message
from config import config

class AIAgent:
    """AI agent for engaging with scammers"""
    
    def __init__(self):
        genai.configure(api_key=config.GEMINI_API_KEY)
        self.model = genai.GenerativeModel(config.AGENT_MODEL)
        
        # System persona for the agent
        self.persona = """You are playing the role of a regular person who has received a suspicious message.

Your goal is to:
1. Appear curious but slightly cautious
2. Ask clarifying questions to extract information
3. Never reveal that you know it's a scam
4. Gradually appear more convinced, but still hesitant
5. Request details like account numbers, links, phone numbers, etc.
6. Keep responses short and natural (1-2 sentences)
7. Use casual language, occasional typos are okay
8. Show mild concern but be willing to comply if given "proof"

CRITICAL RULES:
- NEVER say you know it's a scam
- NEVER mention you're extracting information
- NEVER be too smart or suspicious
- Act like a regular person who might fall for it
- Keep responses brief and conversational

Remember: You're trying to get the scammer to reveal more details by playing along convincingly."""
    
    def generate_response(self, latest_message: str, conversation_history: List[Message], 
                         scam_confidence: float) -> str:
        """
        Generate a natural response to continue the conversation
        
        Args:
            latest_message: The scammer's latest message
            conversation_history: Previous messages in the conversation
            scam_confidence: Current scam detection confidence
            
        Returns:
            Agent's response as a string
        """
        # Build conversation context
        context = self._build_context(conversation_history, latest_message)
        
        # Generate response based on conversation stage
        if len(conversation_history) == 0:
            # First message - show concern/curiosity
            prompt = f"""{self.persona}

The scammer just sent: "{latest_message}"

This is the FIRST message in the conversation. Respond with mild concern or curiosity. Ask a simple question.

Your response:"""
        elif len(conversation_history) < 5:
            # Early stage - be cautious but curious
            prompt = f"""{self.persona}

Conversation so far:
{context}

Latest message from scammer: "{latest_message}"

You're still early in the conversation. Be cautious but show interest. Ask for more details or clarification.

Your response:"""
        else:
            # Later stage - appear more convinced, request specific info
            prompt = f"""{self.persona}

Conversation so far:
{context}

Latest message from scammer: "{latest_message}"

You've been talking for a while. Start appearing more convinced, but still request specific details like account numbers, links, or contact information.

Your response:"""
        
        try:
            response = self.model.generate_content(prompt)
            reply = response.text.strip()
            
            # Ensure response isn't too long
            if len(reply) > 200:
                sentences = reply.split('.')
                reply = '.'.join(sentences[:2]) + '.'
            
            return reply
        
        except Exception as e:
            # Fallback responses if API fails
            fallback_responses = [
                "Why is this happening?",
                "Can you explain more?",
                "What do I need to do?",
                "Is this really urgent?",
                "How do I verify this?"
            ]
            return fallback_responses[len(conversation_history) % len(fallback_responses)]
    
    def _build_context(self, conversation_history: List[Message], latest_message: str) -> str:
        """Build conversation context for the prompt"""
        context_lines = []
        
        # Include last 10 messages max to avoid token limits
        recent_history = conversation_history[-10:] if len(conversation_history) > 10 else conversation_history
        
        for msg in recent_history:
            sender_label = "Scammer" if msg.sender == "scammer" else "You"
            # Handle both Message objects and dicts
            text = msg.text if hasattr(msg, 'text') else msg.get('text', '')
            context_lines.append(f"{sender_label}: {text}")
        
        return "\n".join(context_lines)
