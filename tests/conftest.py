"""Pytest configuration and fixtures"""
import pytest
import os
import sys
import types
from pathlib import Path


# Stub the allosaurus dependency so unit tests can run without the heavy model
# present. Individual tests can monkeypatch ``read_recognizer`` with a concrete
# implementation when needed.
allosaurus_stub = types.ModuleType("allosaurus")
allosaurus_app_stub = types.ModuleType("allosaurus.app")


def _stub_read_recognizer(_model_name):  # pragma: no cover - defensive default
    raise RuntimeError("allosaurus recognizer not available in test environment")


allosaurus_app_stub.read_recognizer = _stub_read_recognizer
allosaurus_stub.app = allosaurus_app_stub
sys.modules.setdefault("allosaurus", allosaurus_stub)
sys.modules.setdefault("allosaurus.app", allosaurus_app_stub)


# Set test environment variables
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY", "test_key_for_ci")


@pytest.fixture
def sample_gurmukhi_text():
    """Sample Gurmukhi text for testing"""
    return "ਤੁਸੀਂ ਕਿਵੇਂ ਹੋ?"


@pytest.fixture
def sample_romanised_text():
    """Sample Romanised Punjabi text"""
    return "tusi kiven ho?"


@pytest.fixture
def sample_english_text():
    """Sample English text"""
    return "How are you?"


@pytest.fixture
def test_audio_dir(tmp_path):
    """Create temporary directory for test audio files"""
    audio_dir = tmp_path / "audio"
    audio_dir.mkdir()
    return audio_dir


@pytest.fixture
def mock_audio_file(tmp_path):
    """Create a mock audio file for testing"""
    # Create a minimal WAV file (44 bytes header + silent audio)
    audio_file = tmp_path / "test_audio.wav"
    
    # Minimal WAV header for a 1-second silent mono 16kHz file
    with open(audio_file, "wb") as f:
        # RIFF header
        f.write(b'RIFF')
        f.write((36 + 16000 * 2).to_bytes(4, 'little'))  # File size - 8
        f.write(b'WAVE')
        
        # fmt chunk
        f.write(b'fmt ')
        f.write((16).to_bytes(4, 'little'))  # Chunk size
        f.write((1).to_bytes(2, 'little'))   # Audio format (PCM)
        f.write((1).to_bytes(2, 'little'))   # Channels (mono)
        f.write((16000).to_bytes(4, 'little'))  # Sample rate
        f.write((32000).to_bytes(4, 'little'))  # Byte rate
        f.write((2).to_bytes(2, 'little'))   # Block align
        f.write((16).to_bytes(2, 'little'))  # Bits per sample
        
        # data chunk
        f.write(b'data')
        f.write((16000 * 2).to_bytes(4, 'little'))  # Data size
        f.write(b'\x00' * (16000 * 2))  # Silent audio data
    
    return audio_file

