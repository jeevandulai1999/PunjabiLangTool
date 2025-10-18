"""Session state management and analytics"""
from typing import Dict, List, Optional
from datetime import datetime
import uuid
import time
import re
from backend.models.session import SessionState, SessionMetrics, SessionSummary
from backend.models.transcript import ConversationTurn, TriScript
from backend.models.scenario import Scenario


class SessionManager:
    """Manages conversation session state and analytics"""
    
    def __init__(self, scenario: Scenario):
        """
        Initialize session manager.
        
        Args:
            scenario: Scenario for this session
        """
        self.session_id = str(uuid.uuid4())
        self.scenario = scenario
        self.state = SessionState.ACTIVE
        self.turns: List[ConversationTurn] = []
        self.conversation_history: List[Dict[str, str]] = []
        self.metrics = SessionMetrics()
        self.started_at = time.time()
        self.completed_at: Optional[float] = None
        
        # Analytics tracking
        self._word_counts: List[int] = []
        self._filler_words = ["um", "uh", "er", "ah", "like", "you know"]
        self._vocab_set = set()
    
    def add_turn(
        self,
        speaker: str,
        transcript: TriScript,
        audio_url: Optional[str] = None,
        confidence: Optional[float] = None
    ) -> None:
        """
        Add a conversation turn.
        
        Args:
            speaker: "user" or "ai"
            transcript: TriScript with gurmukhi, romanised, english
            audio_url: Optional audio URL for AI turns
            confidence: Optional ASR confidence for user turns
        """
        turn = ConversationTurn(
            speaker=speaker,
            transcript=transcript,
            audio_url=audio_url,
            timestamp=time.time(),
            confidence=confidence
        )
        
        self.turns.append(turn)
        
        # Add to conversation history for LLM context
        self.conversation_history.append({
            "role": "user" if speaker == "user" else "assistant",
            "content": transcript.gurmukhi
        })
        
        # Update metrics
        self.metrics.turn_count += 1
        
        if speaker == "user":
            self._update_user_metrics(transcript, confidence)
    
    def _update_user_metrics(
        self,
        transcript: TriScript,
        confidence: Optional[float]
    ) -> None:
        """
        Update metrics for user turn.
        
        Args:
            transcript: User transcript
            confidence: ASR confidence score
        """
        # Count words (using romanised for easier processing)
        words = transcript.romanised.lower().split()
        word_count = len(words)
        self._word_counts.append(word_count)
        self.metrics.total_words += word_count
        
        # Count fillers
        filler_count = sum(
            1 for word in words
            if word in self._filler_words
        )
        self.metrics.filler_count += filler_count
        
        # Track unique vocabulary (content words)
        # Simple approach: exclude common fillers and very short words
        content_words = [
            word for word in words
            if len(word) > 2 and word not in self._filler_words
        ]
        self._vocab_set.update(content_words)
        self.metrics.unique_vocab_count = len(self._vocab_set)
        
        # Update confidence tracking
        if confidence is not None:
            if self.metrics.average_confidence is None:
                self.metrics.average_confidence = confidence
            else:
                # Running average
                n = len([t for t in self.turns if t.speaker == "user"])
                self.metrics.average_confidence = (
                    (self.metrics.average_confidence * (n - 1) + confidence) / n
                )
    
    def calculate_wpm(self) -> Optional[float]:
        """
        Calculate words per minute for user speech.
        
        Returns:
            Words per minute or None if not enough data
        """
        if not self._word_counts or self.metrics.total_duration_seconds < 10:
            return None
        
        # Calculate duration from user turns (approximate)
        user_turn_count = len([t for t in self.turns if t.speaker == "user"])
        if user_turn_count == 0:
            return None
        
        # Estimate speaking time (rough approximation)
        # Assume average turn takes 5 seconds
        estimated_speaking_seconds = user_turn_count * 5
        
        wpm = (self.metrics.total_words / estimated_speaking_seconds) * 60
        return round(wpm, 1)
    
    def pause(self) -> None:
        """Pause the session (e.g., for help mode)"""
        self.state = SessionState.PAUSED
    
    def resume(self) -> None:
        """Resume the session"""
        self.state = SessionState.ACTIVE
    
    def enter_help_mode(self) -> None:
        """Enter help mode"""
        self.state = SessionState.HELP_MODE
        self.metrics.help_invocations += 1
    
    def exit_help_mode(self) -> None:
        """Exit help mode and resume"""
        self.state = SessionState.ACTIVE
    
    def complete(self, confidence_rating: Optional[int] = None) -> SessionSummary:
        """
        Complete the session and generate summary.
        
        Args:
            confidence_rating: User self-reported confidence (1-5)
        
        Returns:
            SessionSummary object
        """
        self.state = SessionState.COMPLETED
        self.completed_at = time.time()
        self.metrics.total_duration_seconds = self.completed_at - self.started_at
        
        # Calculate final WPM
        wpm = self.calculate_wpm()
        if wpm is not None:
            self.metrics.words_per_minute = wpm
        
        return SessionSummary(
            session_id=self.session_id,
            scenario_id=self.scenario.id,
            scenario_title=self.scenario.title,
            metrics=self.metrics,
            confidence_rating=confidence_rating,
            started_at=self.started_at,
            completed_at=self.completed_at
        )
    
    def get_recent_context(self, num_turns: int = 5) -> str:
        """
        Get recent conversation context for help mode.
        
        Args:
            num_turns: Number of recent turns to include
        
        Returns:
            Formatted context string
        """
        recent_turns = self.turns[-num_turns:]
        context_lines = []
        
        for turn in recent_turns:
            speaker_label = "You" if turn.speaker == "user" else self.scenario.persona_name
            context_lines.append(
                f"{speaker_label}: {turn.transcript.gurmukhi} "
                f"({turn.transcript.romanised}) - {turn.transcript.english}"
            )
        
        return "\n".join(context_lines)


# Active sessions storage (in-memory for MVP)
_active_sessions: Dict[str, SessionManager] = {}


def create_session(scenario: Scenario) -> SessionManager:
    """
    Create new session.
    
    Args:
        scenario: Scenario for the session
    
    Returns:
        SessionManager instance
    """
    session = SessionManager(scenario)
    _active_sessions[session.session_id] = session
    return session


def get_session(session_id: str) -> Optional[SessionManager]:
    """
    Get active session by ID.
    
    Args:
        session_id: Session identifier
    
    Returns:
        SessionManager or None if not found
    """
    return _active_sessions.get(session_id)


def end_session(session_id: str) -> None:
    """
    End and remove session.
    
    Args:
        session_id: Session identifier
    """
    if session_id in _active_sessions:
        del _active_sessions[session_id]

