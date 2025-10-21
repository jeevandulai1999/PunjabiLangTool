"""Tests for data models"""
import pytest
from backend.models.transcript import TriScript, TranscriptWithConfidence, ConversationTurn
from backend.models.vowel_feedback import VowelFeedback, VowelAssessment, VowelScoreDetails
from backend.models.scenario import Scenario
from backend.models.session import SessionMetrics, SessionState


class TestTriScript:
    """Test TriScript model"""
    
    def test_create_triscript(
        self,
        sample_gurmukhi_text,
        sample_romanised_text,
        sample_english_text
    ):
        """Test creating a TriScript instance"""
        triscript = TriScript(
            gurmukhi=sample_gurmukhi_text,
            romanised=sample_romanised_text,
            english=sample_english_text
        )
        
        assert triscript.gurmukhi == sample_gurmukhi_text
        assert triscript.romanised == sample_romanised_text
        assert triscript.english == sample_english_text
    
    def test_triscript_dict(self, sample_gurmukhi_text):
        """Test TriScript serialization"""
        triscript = TriScript(
            gurmukhi=sample_gurmukhi_text,
            romanised="test",
            english="test"
        )
        
        data = triscript.model_dump()
        assert isinstance(data, dict)
        assert "gurmukhi" in data
        assert "romanised" in data
        assert "english" in data


class TestTranscriptWithConfidence:
    """Test TranscriptWithConfidence model"""
    
    def test_with_confidence(self):
        """Test transcript with confidence score"""
        transcript = TranscriptWithConfidence(
            gurmukhi="ਟੈਸਟ",
            romanised="test",
            english="test",
            confidence=0.95,
            duration_seconds=2.5
        )
        
        assert transcript.confidence == 0.95
        assert transcript.duration_seconds == 2.5
    
    def test_optional_confidence(self):
        """Test that confidence is optional"""
        transcript = TranscriptWithConfidence(
            gurmukhi="ਟੈਸਟ",
            romanised="test",
            english="test"
        )

        assert transcript.confidence is None
        assert transcript.duration_seconds is None

    def test_vowel_feedback_optional(self):
        """Transcript should allow optional vowel feedback"""
        transcript = TranscriptWithConfidence(
            gurmukhi="ਟੈਸਟ",
            romanised="test",
            english="test",
        )

        assert transcript.vowel_feedback is None

    def test_vowel_feedback_assignment(self):
        """Transcript should accept vowel feedback payload"""
        assessment = VowelAssessment(
            expected_vowel="ਅ",
            detected_cluster=None,
            confidence=0.0,
            match=False,
            scores=VowelScoreDetails(overall_score=0.0)
        )
        feedback = VowelFeedback(assessments={"ਅ": assessment})
        transcript = TranscriptWithConfidence(
            gurmukhi="ਟੈਸਟ",
            romanised="test",
            english="test",
            vowel_feedback=feedback,
        )

        assert transcript.vowel_feedback is feedback


class TestScenario:
    """Test Scenario model"""
    
    def test_create_scenario(self):
        """Test creating a Scenario"""
        scenario = Scenario(
            id="test_scenario",
            title="Test Scenario",
            description="A test scenario",
            persona_name="Test Person",
            persona_role="Tester",
            persona_description="A test persona",
            setting="Test setting",
            goals=["Goal 1", "Goal 2"],
            dialect="doabi"
        )
        
        assert scenario.id == "test_scenario"
        assert scenario.title == "Test Scenario"
        assert len(scenario.goals) == 2
        assert scenario.dialect == "doabi"


class TestSessionMetrics:
    """Test SessionMetrics model"""
    
    def test_default_metrics(self):
        """Test default metric values"""
        metrics = SessionMetrics()
        
        assert metrics.total_words == 0
        assert metrics.filler_count == 0
        assert metrics.unique_vocab_count == 0
        assert metrics.help_invocations == 0
        assert metrics.turn_count == 0
        assert metrics.total_duration_seconds == 0.0
    
    def test_update_metrics(self):
        """Test updating metrics"""
        metrics = SessionMetrics(
            total_words=50,
            filler_count=3,
            unique_vocab_count=25,
            words_per_minute=120.5
        )
        
        assert metrics.total_words == 50
        assert metrics.filler_count == 3
        assert metrics.unique_vocab_count == 25
        assert metrics.words_per_minute == 120.5


class TestConversationTurn:
    """Test ConversationTurn model"""
    
    def test_create_user_turn(self):
        """Test creating a user turn"""
        transcript = TriScript(
            gurmukhi="ਟੈਸਟ",
            romanised="test",
            english="test"
        )
        
        turn = ConversationTurn(
            speaker="user",
            transcript=transcript,
            timestamp=1234567890.0,
            confidence=0.9
        )
        
        assert turn.speaker == "user"
        assert turn.confidence == 0.9
        assert turn.audio_url is None
    
    def test_create_ai_turn(self):
        """Test creating an AI turn"""
        transcript = TriScript(
            gurmukhi="ਟੈਸਟ",
            romanised="test",
            english="test"
        )
        
        turn = ConversationTurn(
            speaker="ai",
            transcript=transcript,
            timestamp=1234567890.0,
            audio_url="/static/audio/test.mp3"
        )
        
        assert turn.speaker == "ai"
        assert turn.audio_url == "/static/audio/test.mp3"
        assert turn.confidence is None

