"""Core OpenAI client wrapper with API key management"""
import os
from typing import Optional
from openai import OpenAI, AsyncOpenAI
from dotenv import load_dotenv


# Load environment variables
load_dotenv()


class OpenAIClientWrapper:
    """Wrapper for OpenAI client with API key from environment"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize OpenAI client.
        
        Args:
            api_key: Optional API key. If not provided, reads from OPENAI_API_KEY env var.
        
        Raises:
            ValueError: If API key is not found in environment or parameter.
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        
        if not self.api_key:
            raise ValueError(
                "OpenAI API key not found. Set OPENAI_API_KEY environment variable."
            )
        
        self._client: Optional[OpenAI] = None
        self._async_client: Optional[AsyncOpenAI] = None
    
    @property
    def client(self) -> OpenAI:
        """Get synchronous OpenAI client (lazy initialization)"""
        if self._client is None:
            self._client = OpenAI(api_key=self.api_key)
        return self._client
    
    @property
    def async_client(self) -> AsyncOpenAI:
        """Get asynchronous OpenAI client (lazy initialization)"""
        if self._async_client is None:
            self._async_client = AsyncOpenAI(api_key=self.api_key)
        return self._async_client


# Global client instance
_global_client: Optional[OpenAIClientWrapper] = None


def get_openai_client() -> OpenAIClientWrapper:
    """
    Get global OpenAI client instance (singleton pattern).
    
    Returns:
        OpenAIClientWrapper instance
    """
    global _global_client
    if _global_client is None:
        _global_client = OpenAIClientWrapper()
    return _global_client


def reset_openai_client() -> None:
    """Reset global client (useful for testing)"""
    global _global_client
    _global_client = None

