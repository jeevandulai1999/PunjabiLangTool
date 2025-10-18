"""OpenAI API usage and cost tracking service"""
from typing import Dict, Optional
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class UsageStats:
    """Track OpenAI API usage statistics"""
    whisper_seconds: float = 0.0
    gpt_input_tokens: int = 0
    gpt_output_tokens: int = 0
    tts_characters: int = 0
    
    # Pricing (as of 2024)
    WHISPER_PRICE_PER_SECOND = 0.0001  # $0.006 per minute = $0.0001 per second
    GPT_35_INPUT_PRICE_PER_1K = 0.0005  # $0.50 per 1M tokens
    GPT_35_OUTPUT_PRICE_PER_1K = 0.0015  # $1.50 per 1M tokens
    GPT_4O_MINI_INPUT_PRICE_PER_1K = 0.00015  # $0.15 per 1M tokens
    GPT_4O_MINI_OUTPUT_PRICE_PER_1K = 0.0006  # $0.60 per 1M tokens
    TTS_PRICE_PER_1K_CHARS = 0.015  # $15 per 1M characters
    
    def add_whisper_usage(self, seconds: float) -> None:
        """Add Whisper API usage"""
        self.whisper_seconds += seconds
    
    def add_gpt_usage(self, input_tokens: int, output_tokens: int) -> None:
        """Add GPT API usage"""
        self.gpt_input_tokens += input_tokens
        self.gpt_output_tokens += output_tokens
    
    def add_tts_usage(self, characters: int) -> None:
        """Add TTS API usage"""
        self.tts_characters += characters
    
    def get_whisper_cost(self) -> float:
        """Calculate Whisper cost"""
        return self.whisper_seconds * self.WHISPER_PRICE_PER_SECOND
    
    def get_gpt_cost(self, model: str = "gpt-3.5-turbo") -> float:
        """Calculate GPT cost based on model"""
        if model.startswith("gpt-4o-mini"):
            input_cost = (self.gpt_input_tokens / 1000) * self.GPT_4O_MINI_INPUT_PRICE_PER_1K
            output_cost = (self.gpt_output_tokens / 1000) * self.GPT_4O_MINI_OUTPUT_PRICE_PER_1K
        else:  # gpt-3.5-turbo
            input_cost = (self.gpt_input_tokens / 1000) * self.GPT_35_INPUT_PRICE_PER_1K
            output_cost = (self.gpt_output_tokens / 1000) * self.GPT_35_OUTPUT_PRICE_PER_1K
        return input_cost + output_cost
    
    def get_tts_cost(self) -> float:
        """Calculate TTS cost"""
        return (self.tts_characters / 1000) * self.TTS_PRICE_PER_1K_CHARS
    
    def get_total_cost(self, model: str = "gpt-3.5-turbo") -> float:
        """Calculate total estimated cost"""
        return self.get_whisper_cost() + self.get_gpt_cost(model) + self.get_tts_cost()
    
    def get_summary(self, model: str = "gpt-3.5-turbo") -> Dict[str, any]:
        """Get usage summary with costs"""
        return {
            "whisper": {
                "seconds": round(self.whisper_seconds, 2),
                "minutes": round(self.whisper_seconds / 60, 2),
                "cost": f"${self.get_whisper_cost():.4f}"
            },
            "gpt": {
                "input_tokens": self.gpt_input_tokens,
                "output_tokens": self.gpt_output_tokens,
                "total_tokens": self.gpt_input_tokens + self.gpt_output_tokens,
                "model": model,
                "cost": f"${self.get_gpt_cost(model):.4f}"
            },
            "tts": {
                "characters": self.tts_characters,
                "cost": f"${self.get_tts_cost():.4f}"
            },
            "total_cost": f"${self.get_total_cost(model):.4f}"
        }


class UsageTracker:
    """Track OpenAI API usage per session"""
    
    def __init__(self):
        """Initialize usage tracker"""
        self.session_stats: Dict[str, UsageStats] = {}
        self.global_stats = UsageStats()
    
    def get_or_create_session_stats(self, session_id: str) -> UsageStats:
        """Get or create usage stats for a session"""
        if session_id not in self.session_stats:
            self.session_stats[session_id] = UsageStats()
        return self.session_stats[session_id]
    
    def track_whisper(self, session_id: str, seconds: float) -> None:
        """Track Whisper API usage"""
        stats = self.get_or_create_session_stats(session_id)
        stats.add_whisper_usage(seconds)
        self.global_stats.add_whisper_usage(seconds)
    
    def track_gpt(self, session_id: str, input_tokens: int, output_tokens: int) -> None:
        """Track GPT API usage"""
        stats = self.get_or_create_session_stats(session_id)
        stats.add_gpt_usage(input_tokens, output_tokens)
        self.global_stats.add_gpt_usage(input_tokens, output_tokens)
    
    def track_tts(self, session_id: str, characters: int) -> None:
        """Track TTS API usage"""
        stats = self.get_or_create_session_stats(session_id)
        stats.add_tts_usage(characters)
        self.global_stats.add_tts_usage(characters)
    
    def get_session_summary(self, session_id: str, model: str = "gpt-3.5-turbo") -> Dict[str, any]:
        """Get usage summary for a session"""
        stats = self.get_or_create_session_stats(session_id)
        return stats.get_summary(model)
    
    def get_global_summary(self, model: str = "gpt-3.5-turbo") -> Dict[str, any]:
        """Get global usage summary"""
        return self.global_stats.get_summary(model)
    
    def check_account_balance(self) -> Optional[Dict[str, any]]:
        """
        Check OpenAI account balance and usage.
        Note: This may not work with all API key types.
        """
        try:
            from backend.services.openai_client import get_openai_client
            import httpx
            
            client = get_openai_client()
            
            headers = {
                "Authorization": f"Bearer {client.api_key}",
                "Content-Type": "application/json"
            }
            
            # Try multiple endpoints to get balance info
            endpoints_to_try = [
                "https://api.openai.com/v1/dashboard/billing/subscription",
                "https://api.openai.com/v1/dashboard/billing/usage",
                "https://api.openai.com/v1/organization/usage",
            ]
            
            for endpoint in endpoints_to_try:
                try:
                    response = httpx.get(endpoint, headers=headers, timeout=5.0)
                    
                    if response.status_code == 200:
                        data = response.json()
                        return {
                            "available": True,
                            "data": data,
                            "endpoint": endpoint,
                            "note": "Balance info retrieved"
                        }
                except Exception:
                    continue
            
            # If none worked, return helpful message
            return {
                "available": False,
                "note": "Balance check not available with your API key type. Visit OpenAI dashboard for details.",
                "link": "https://platform.openai.com/account/billing"
            }
                
        except Exception as e:
            return {
                "available": False,
                "note": "Unable to check balance automatically. Visit OpenAI dashboard.",
                "link": "https://platform.openai.com/account/billing",
                "error": str(e)
            }


# Global tracker instance
_usage_tracker: Optional[UsageTracker] = None


def get_usage_tracker() -> UsageTracker:
    """Get global usage tracker instance (singleton pattern)"""
    global _usage_tracker
    if _usage_tracker is None:
        _usage_tracker = UsageTracker()
    return _usage_tracker

