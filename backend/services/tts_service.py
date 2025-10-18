"""Text-to-Speech service using OpenAI TTS"""
from typing import Optional, BinaryIO
from pathlib import Path
from backend.services.openai_client import get_openai_client


class TTSService:
    """Service for text-to-speech using OpenAI TTS"""
    
    def __init__(
        self,
        model: str = "tts-1",
        voice: str = "alloy"
    ):
        """
        Initialize TTS service.
        
        Args:
            model: OpenAI TTS model ("tts-1" for faster, "tts-1-hd" for higher quality)
            voice: Voice to use (alloy, echo, fable, onyx, nova, shimmer)
        """
        self.client = get_openai_client()
        self.model = model
        self.voice = voice
    
    def generate_speech(
        self,
        text: str,
        output_path: Optional[str | Path] = None,
        voice: Optional[str] = None,
        speed: float = 1.0
    ) -> bytes:
        """
        Generate speech from text.
        
        Args:
            text: Text to convert to speech (Punjabi in Gurmukhi script)
            output_path: Optional path to save audio file
            voice: Optional voice override
            speed: Speech speed (0.25 to 4.0)
        
        Returns:
            Audio data as bytes
        """
        response = self.client.client.audio.speech.create(
            model=self.model,
            voice=voice or self.voice,
            input=text,
            speed=speed
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
        speed: float = 1.0
    ) -> bytes:
        """
        Async version of speech generation.
        
        Args:
            text: Text to convert to speech (Punjabi in Gurmukhi script)
            output_path: Optional path to save audio file
            voice: Optional voice override
            speed: Speech speed (0.25 to 4.0)
        
        Returns:
            Audio data as bytes
        """
        response = await self.client.async_client.audio.speech.create(
            model=self.model,
            voice=voice or self.voice,
            input=text,
            speed=speed
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
        speed: float = 1.0
    ):
        """
        Stream speech generation (for real-time playback).
        
        Args:
            text: Text to convert to speech
            voice: Optional voice override
            speed: Speech speed
        
        Yields:
            Audio data chunks
        """
        response = self.client.client.audio.speech.create(
            model=self.model,
            voice=voice or self.voice,
            input=text,
            speed=speed
        )
        
        # Stream response
        yield from response.iter_bytes()


# Global service instance
_tts_service: Optional[TTSService] = None


def get_tts_service(
    model: str = "tts-1",
    voice: str = "alloy"
) -> TTSService:
    """
    Get global TTS service instance (singleton pattern).
    
    Args:
        model: TTS model to use
        voice: Voice to use
    
    Returns:
        TTSService instance
    """
    global _tts_service
    if _tts_service is None:
        _tts_service = TTSService(model=model, voice=voice)
    return _tts_service

