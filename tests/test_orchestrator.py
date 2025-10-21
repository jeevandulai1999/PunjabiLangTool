"""Tests for the conversation orchestrator phoneme integration."""

from io import BytesIO
from types import SimpleNamespace

from backend.services import orchestrator as orchestrator_module
from backend.models.transcript import PhonemePrediction
from backend.models.vowel_feedback import VowelFeedback


class DummySession:
    session_id = "session-123"

    def get_recent_context(self, num_turns=0):
        return "context"


class DummyASRService:
    def transcribe_audio(self, audio_file):
        # ensure we can read the bytes that were fanned out
        assert audio_file.read() == b"audio"
        audio_file.seek(0)
        return {
            "text": "ਸਤ ਸ੍ਰੀ ਅਕਾਲ",
            "language": "pa",
            "duration": 1.23,
            "segments": [
                {"no_speech_prob": 0.1},
                {"no_speech_prob": 0.2},
            ],
        }

    def get_average_confidence(self, transcription):
        return 0.75


class DummyPhonemeService:
    def extract_phonemes(self, audio_file):
        assert audio_file.read() == b"audio"
        return [PhonemePrediction(phoneme="s", start=0.0, end=0.1, confidence=0.9)]


class DummyTranslationService:
    def translate_punjabi_to_english(self, text, context="", session_id=""):
        return "hello"


class DummyUsageTracker:
    def track_whisper(self, session_id, duration):
        self.called_with = (session_id, duration)

    def track_gpt(self, *args, **kwargs):
        pass

    def track_tts(self, *args, **kwargs):
        pass

    def track_phoneme_analysis(self, session_id, seconds):
        self.phoneme_called_with = (session_id, seconds)

    def track_vowel_analysis(self, session_id, seconds):
        self.vowel_called_with = (session_id, seconds)


def test_process_user_audio_includes_phonemes(monkeypatch):
    monkeypatch.setattr(orchestrator_module, "get_asr_service", lambda: DummyASRService())
    monkeypatch.setattr(orchestrator_module, "get_translation_service", lambda: DummyTranslationService())
    monkeypatch.setattr(orchestrator_module, "get_conversation_service", lambda: SimpleNamespace())
    monkeypatch.setattr(orchestrator_module, "get_tts_service", lambda: SimpleNamespace())
    monkeypatch.setattr(orchestrator_module, "get_help_service", lambda: SimpleNamespace())
    monkeypatch.setattr(orchestrator_module, "get_scenario_service", lambda: SimpleNamespace())
    tracker = DummyUsageTracker()
    monkeypatch.setattr(orchestrator_module, "get_usage_tracker", lambda: tracker)
    monkeypatch.setattr(orchestrator_module, "get_phoneme_service", lambda: DummyPhonemeService())

    convo_orchestrator = orchestrator_module.ConversationOrchestrator()
    convo_orchestrator._get_romanisation_from_llm = lambda *args, **kwargs: "sat sri akaal"

    audio = BytesIO(b"audio")
    audio.name = "audio.wav"
    result = convo_orchestrator.process_user_audio(audio, DummySession())

    assert result.gurmukhi == "ਸਤ ਸ੍ਰੀ ਅਕਾਲ"
    assert result.english == "hello"
    assert result.phonemes is not None
    assert len(result.phonemes) == 1
    assert result.phonemes[0].phoneme == "s"
    assert isinstance(result.vowel_feedback, VowelFeedback)
    assert hasattr(tracker, "phoneme_called_with")
    assert hasattr(tracker, "vowel_called_with")

