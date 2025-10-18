"""Tests for session manager"""
import pytest
import time
from backend.models.scenario import Scenario
from backend.models.transcript import TriScript
from backend.services.session_manager import SessionManager, create_session, get_session


@pytest.fixture
def test_scenario():
    """Create a test scenario"""
    return Scenario(
        id="test_scenario",
        title="Test Scenario",
        description="A test scenario for testing",
        persona_name="Test Person",
        persona_role="Tester",
        persona_description="A friendly test persona",
        setting="Test environment",
        goals=["Test goal 1", "Test goal 2"],
        dialect="doabi"
    )


class TestSessionManager:
    """Test SessionManager class"""
    
    def test_create_session(self, test_scenario):
        """Test session creation"""
        session = SessionManager(test_scenario)
        
        assert session.session_id is not None
        assert session.scenario == test_scenario
        assert session.state.value == "active"
        assert len(session.turns) == 0
        assert session.metrics.turn_count == 0
    
    def test_add_user_turn(self, test_scenario):
        """Test adding a user turn"""
        session = SessionManager(test_scenario)
        
        transcript = TriScript(
            gurmukhi="ਟੈਸਟ",
            romanised="test word",
            english="test word"
        )
        
        session.add_turn(
            speaker="user",
            transcript=transcript,
            confidence=0.95
        )
        
        assert len(session.turns) == 1
        assert session.turns[0].speaker == "user"
        assert session.metrics.turn_count == 1
        assert session.metrics.total_words == 2  # "test word"
    
    def test_add_ai_turn(self, test_scenario):
        """Test adding an AI turn"""
        session = SessionManager(test_scenario)
        
        transcript = TriScript(
            gurmukhi="ਟੈਸਟ",
            romanised="test",
            english="test"
        )
        
        session.add_turn(
            speaker="ai",
            transcript=transcript,
            audio_url="/test.mp3"
        )
        
        assert len(session.turns) == 1
        assert session.turns[0].speaker == "ai"
        assert session.turns[0].audio_url == "/test.mp3"
        assert session.metrics.turn_count == 1
    
    def test_filler_counting(self, test_scenario):
        """Test filler word counting"""
        session = SessionManager(test_scenario)
        
        transcript = TriScript(
            gurmukhi="ਟੈਸਟ",
            romanised="um well uh test like you know",
            english="test"
        )
        
        session.add_turn(
            speaker="user",
            transcript=transcript,
            confidence=0.9
        )
        
        # Should count: um, uh, like, you know (4 fillers)
        assert session.metrics.filler_count >= 2  # At least some fillers detected
    
    def test_unique_vocab_tracking(self, test_scenario):
        """Test unique vocabulary tracking"""
        session = SessionManager(test_scenario)
        
        # First turn with "hello world"
        transcript1 = TriScript(
            gurmukhi="ਟੈਸਟ",
            romanised="hello world",
            english="hello world"
        )
        session.add_turn(speaker="user", transcript=transcript1)
        
        # Second turn with "hello" again and new word "test"
        transcript2 = TriScript(
            gurmukhi="ਟੈਸਟ",
            romanised="hello test",
            english="hello test"
        )
        session.add_turn(speaker="user", transcript=transcript2)
        
        # Should have 3 unique words: hello, world, test
        assert session.metrics.unique_vocab_count >= 3
    
    def test_pause_resume(self, test_scenario):
        """Test pausing and resuming session"""
        session = SessionManager(test_scenario)
        
        assert session.state.value == "active"
        
        session.pause()
        assert session.state.value == "paused"
        
        session.resume()
        assert session.state.value == "active"
    
    def test_help_mode(self, test_scenario):
        """Test help mode transitions"""
        session = SessionManager(test_scenario)
        
        assert session.metrics.help_invocations == 0
        
        session.enter_help_mode()
        assert session.state.value == "help_mode"
        assert session.metrics.help_invocations == 1
        
        session.exit_help_mode()
        assert session.state.value == "active"
    
    def test_session_completion(self, test_scenario):
        """Test session completion"""
        session = SessionManager(test_scenario)
        
        # Add some turns
        transcript = TriScript(
            gurmukhi="ਟੈਸਟ",
            romanised="test",
            english="test"
        )
        session.add_turn(speaker="user", transcript=transcript)
        session.add_turn(speaker="ai", transcript=transcript)
        
        # Complete session
        summary = session.complete(confidence_rating=4)
        
        assert session.state.value == "completed"
        assert summary.session_id == session.session_id
        assert summary.confidence_rating == 4
        assert summary.completed_at is not None
    
    def test_get_recent_context(self, test_scenario):
        """Test getting recent conversation context"""
        session = SessionManager(test_scenario)
        
        # Add some turns
        for i in range(10):
            transcript = TriScript(
                gurmukhi=f"ਟੈਸਟ{i}",
                romanised=f"test{i}",
                english=f"test{i}"
            )
            session.add_turn(
                speaker="user" if i % 2 == 0 else "ai",
                transcript=transcript
            )
        
        # Get recent context (default 5 turns)
        context = session.get_recent_context(num_turns=5)
        
        assert context
        assert "test" in context.lower()
    
    def test_create_and_get_session(self, test_scenario):
        """Test session creation and retrieval"""
        session = create_session(test_scenario)
        
        retrieved = get_session(session.session_id)
        assert retrieved is not None
        assert retrieved.session_id == session.session_id
        
        # Non-existent session
        assert get_session("nonexistent") is None

