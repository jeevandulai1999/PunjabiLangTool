"""Unit tests for the phoneme extraction service."""

from types import SimpleNamespace
from io import BytesIO
import math

from backend.services import phoneme_service


class DummyAudioSegment:
    """Lightweight stub used to avoid relying on ffmpeg in tests."""

    def set_channels(self, _channels):
        return self

    def set_frame_rate(self, _frame_rate):
        return self

    def export(self, file_obj, format="wav"):
        assert format == "wav"
        file_obj.write(b"RIFF0000WAVEfmt ")


def test_extract_phonemes_returns_time_aligned_segments(monkeypatch):
    """The service should return normalised phoneme dictionaries."""

    dummy_segment = SimpleNamespace(log_prob=-0.1, start=0.0, end=0.12, token="p")

    class DummyRecognizer:
        def recognize(self, file_path, lang_id=None, timestamp=False):
            assert file_path.endswith(".wav")
            assert timestamp is True
            assert lang_id == "ipa"
            return [dummy_segment]

    monkeypatch.setattr(phoneme_service, "read_recognizer", lambda model: DummyRecognizer())
    monkeypatch.setattr(phoneme_service.AudioSegment, "from_file", lambda _: DummyAudioSegment())

    service = phoneme_service.PhonemeService()

    audio = BytesIO(b"fake audio stream")
    results = service.extract_phonemes(audio)

    assert len(results) == 1
    segment = results[0]
    assert segment.phoneme == "p"
    assert math.isclose(segment.start or 0.0, 0.0)
    assert math.isclose(segment.end or 0.0, 0.12)
    assert math.isclose(segment.confidence or 0.0, math.exp(-0.1), rel_tol=1e-5)
