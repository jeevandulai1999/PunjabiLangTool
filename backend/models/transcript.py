"""Tri-script transcript data models"""
from typing import Optional
from pydantic import BaseModel, Field


class TriScript(BaseModel):
    """Represents text in three scripts: Gurmukhi, Romanised, and English"""
    
    gurmukhi: str = Field(description="Punjabi text in Gurmukhi script")
    romanised: str = Field(description="Punjabi text in Romanised/Latin script")
    english: str = Field(description="English translation/meaning")
    
    class Config:
        json_schema_extra = {
            "example": {
                "gurmukhi": "ਤੁਸੀਂ ਕਿਵੇਂ ਹੋ?",
                "romanised": "tusi kiven ho?",
                "english": "How are you?"
            }
        }


class TranscriptWithConfidence(TriScript):
    """Transcript with ASR confidence metrics"""
    
    confidence: Optional[float] = Field(
        default=None,
        ge=0.0,
        le=1.0,
        description="ASR confidence score (0-1)"
    )
    duration_seconds: Optional[float] = Field(
        default=None,
        ge=0.0,
        description="Audio duration in seconds"
    )


class ConversationTurn(BaseModel):
    """A single turn in the conversation"""
    
    speaker: str = Field(description="'user' or 'ai'")
    transcript: TriScript
    audio_url: Optional[str] = Field(
        default=None,
        description="URL/path to audio file for AI turns"
    )
    timestamp: float = Field(description="Unix timestamp of turn")
    confidence: Optional[float] = Field(default=None, description="ASR confidence for user turns")

