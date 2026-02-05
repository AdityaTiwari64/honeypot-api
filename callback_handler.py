import requests
from models import FinalResultPayload
from config import config
import logging

logger = logging.getLogger(__name__)

class CallbackHandler:
    """Handles callback to GUVI evaluation endpoint"""
    
    def __init__(self):
        self.callback_url = config.GUVI_CALLBACK_URL
    
    def send_final_result(self, payload: FinalResultPayload) -> tuple[bool, str]:
        """
        Send final intelligence results to GUVI evaluation endpoint
        
        Args:
            payload: FinalResultPayload with all extracted intelligence
            
        Returns:
            Tuple of (success: bool, message: str)
        """
        try:
            response = requests.post(
                self.callback_url,
                json=payload.model_dump(),
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            
            if response.status_code == 200:
                logger.info(f"Successfully sent callback for session {payload.sessionId}")
                return True, "Callback sent successfully"
            else:
                error_msg = f"Callback failed with status {response.status_code}: {response.text}"
                logger.error(error_msg)
                return False, error_msg
        
        except requests.exceptions.Timeout:
            error_msg = "Callback request timed out"
            logger.error(error_msg)
            return False, error_msg
        
        except requests.exceptions.RequestException as e:
            error_msg = f"Callback request failed: {str(e)}"
            logger.error(error_msg)
            return False, error_msg
        
        except Exception as e:
            error_msg = f"Unexpected error during callback: {str(e)}"
            logger.error(error_msg)
            return False, error_msg

callback_handler = CallbackHandler()
