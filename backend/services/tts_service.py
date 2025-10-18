"""Text-to-Speech service using OpenAI TTS"""
from typing import Optional, BinaryIO
from pathlib import Path
import os
from backend.services.openai_client import get_openai_client

# TTS Configuration from environment or defaults
VALID_VOICES = ["nova", "shimmer", "echo", "onyx", "fable", "alloy", "ash", "sage", "coral"]
TTS_MODEL = os.getenv("TTS_MODEL", "tts-1")  # Fast model, high quality
TTS_VOICE = os.getenv("TTS_VOICE", "nova").lower()  # Ensure lowercase
TTS_SPEED = float(os.getenv("TTS_SPEED", "1.0"))  # Normal speed

# Validate voice
if TTS_VOICE not in VALID_VOICES:
    print(f"WARNING: Invalid TTS_VOICE '{TTS_VOICE}'. Using 'nova' instead.")
    TTS_VOICE = "nova"


class TTSService:
    """Service for text-to-speech using OpenAI TTS"""
    
    def __init__(
        self,
        model: str = TTS_MODEL,
        voice: str = TTS_VOICE
    ):
        """
        Initialize TTS service.
        
        Args:
            model: OpenAI TTS model ("tts-1" for faster, "tts-1-hd" for higher quality)
            voice: Voice to use (alloy, echo, fable, onyx, nova, shimmer)
                   For Punjabi, "nova" (female) or "onyx" (male) work best
        """
        self.client = get_openai_client()
        self.model = model
        self.voice = voice
        self.default_speed = TTS_SPEED
    
    def generate_speech(
        self,
        text: str,
        output_path: Optional[str | Path] = None,
        voice: Optional[str] = None,
        speed: Optional[float] = None
    ) -> bytes:
        """
        Generate speech from text.
        
        Args:
            text: Text to convert to speech (Punjabi in Gurmukhi script)
            output_path: Optional path to save audio file
            voice: Optional voice override
            speed: Speech speed (0.25 to 4.0, default 0.95 for natural Punjabi)
        
        Returns:
            Audio data as bytes
        """
        # Use default speed if not specified (slightly slower for clearer Punjabi)
        if speed is None:
            speed = self.default_speed
            
        response = self.client.client.audio.speech.create(
            model=self.model,
            voice=voice or self.voice,
            input=text,
            speed=speed,
            response_format="mp3"  # Explicit format
        )
        
        # Get audio bytes
        audio_data = response.content
        
        # Save to file if path provided
        if output_path:
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, "wb") as f:
                f.write(audio_data)
        
        return audio_data
    
    async def generate_speech_async(
        self,
        text: str,
        output_path: Optional[str | Path] = None,
        voice: Optional[str] = None,
        speed: float = 0.95
    ) -> bytes:
        """
        Async version of speech generation.
        
        Args:
            text: Text to convert to speech (Punjabi in Gurmukhi script)
            output_path: Optional path to save audio file
            voice: Optional voice override
            speed: Speech speed (0.25 to 4.0, default 0.95 for natural Punjabi)
        
        Returns:
            Audio data as bytes
        """
        response = await self.client.async_client.audio.speech.create(
            model=self.model,
            voice=voice or self.voice,
            input=text,
            speed=speed,
            response_format="mp3"
        )
        
        audio_data = response.content
        
        if output_path:
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, "wb") as f:
                f.write(audio_data)
        
        return audio_data
    
    def stream_speech(
        self,
        text: str,
        voice: Optional[str] = None,
        speed: float = 0.95
    ):
        """
        Stream speech generation (for real-time playback).
        
        Args:
            text: Text to convert to speech
            voice: Optional voice override
            speed: Speech speed (default 0.95 for natural Punjabi)
        
        Yields:
            Audio data chunks
        """
        response = self.client.client.audio.speech.create(
            model=self.model,
            voice=voice or self.voice,
            input=text,
            speed=speed,
            response_format="mp3"
        )
        
        # Stream response
        yield from response.iter_bytes()


# Global service instance
_tts_service: Optional[TTSService] = None


def get_tts_service(
    model: str = TTS_MODEL,
    voice: str = TTS_VOICE
) -> TTSService:
    """
    Get global TTS service instance (singleton pattern).
    
    Args:
        model: TTS model to use (tts-1-hd for better quality)
        voice: Voice to use (nova/onyx recommended for Punjabi)
    
    Returns:
        TTSService instance
    """
    global _tts_service
    if _tts_service is None:
        _tts_service = TTSService(model=model, voice=voice)
    return _tts_service

