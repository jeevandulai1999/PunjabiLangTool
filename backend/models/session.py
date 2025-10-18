"""Session and analytics data models"""
from typing import List, Optional
from pydantic import BaseModel, Field
from enum import Enum


class SessionState(str, Enum):
    """Session state enumeration"""
    ACTIVE = "active"
    PAUSED = "paused"
    HELP_MODE = "help_mode"
    COMPLETED = "completed"


class SessionMetrics(BaseModel):
    """Analytics metrics for a session"""
    
    words_per_minute: Optional[float] = Field(default=None, description="User speaking rate")
    total_words: int = Field(default=0, description="Total words spoken by user")
    filler_count: int = Field(default=0, description="Count of filler words (um, uh, etc)")
    unique_vocab_count: int = Field(default=0, description="Unique content words used")
    help_invocations: int = Field(default=0, description="Number of help mode uses")
    turn_count: int = Field(default=0, description="Number of conversation turns")
    total_duration_seconds: float = Field(default=0.0, description="Total session duration")
    average_confidence: Optional[float] = Field(
        default=None,
        description="Average ASR confidence"
    )


class SessionSummary(BaseModel):
    """Summary view for a completed session"""
    
    session_id: str
    scenario_id: str
    scenario_title: str
    metrics: SessionMetrics
    confidence_rating: Optional[int] = Field(
        default=None,
        ge=1,
        le=5,
        description="User self-reported confidence (1-5)"
    )
    started_at: float = Field(description="Unix timestamp")
    completed_at: Optional[float] = Field(default=None, description="Unix timestamp")


class HelpRequest(BaseModel):
    """Help mode request"""
    
    query: str = Field(description="User's help question")
    context: Optional[str] = Field(
        default=None,
        description="Recent conversation context"
    )
    topic: Optional[str] = Field(
        default=None,
        description="Help topic: grammar, vocabulary, culture, alternatives"
    )

