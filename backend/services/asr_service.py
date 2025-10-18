"""Automatic Speech Recognition service using OpenAI Whisper"""
from typing import Optional, BinaryIO
from pathlib import Path
from backend.services.openai_client import get_openai_client


class ASRService:
    """Service for speech-to-text transcription using Whisper"""
    
    def __init__(self):
        """Initialize ASR service with OpenAI client"""
        self.client = get_openai_client()
    
    def transcribe_audio(
        self,
        audio_file: BinaryIO,
        language: str = None,  # Let Whisper auto-detect language
        response_format: str = "verbose_json"
    ) -> dict:
        """
        Transcribe audio file to Punjabi text using Whisper.
        
        Args:
            audio_file: Audio file object (must be open in binary mode)
            language: Language code (default: None for auto-detection)
            response_format: Response format ("verbose_json" for detailed info)
        
        Returns:
            Dictionary containing transcription and metadata:
            {
                "text": str,  # Transcribed text in Gurmukhi
                "language": str,
                "duration": float,
                "segments": list,  # Detailed segments with timestamps
            }
        """
        # Build parameters, only include language if specified
        params = {
            "model": "whisper-1",
            "file": audio_file,
            "response_format": response_format,
            # Add a prompt to hint that it's Punjabi - helps with language detection
            "prompt": "ਸਤ ਸ੍ਰੀ ਅਕਾਲ। ਇਹ ਪੰਜਾਬੀ ਭਾਸ਼ਾ ਦੀ ਗੱਲਬਾਤ ਹੈ।"  # "Sat Sri Akal. This is Punjabi language conversation."
        }
        
        # Only add language parameter if it's provided and supported
        # Whisper auto-detects language, but prompt helps guide it to Punjabi
        if language:
            params["language"] = language
        
        response = self.client.client.audio.transcriptions.create(**params)
        
        # Convert response to dict if needed
        if hasattr(response, 'model_dump'):
            return response.model_dump()
        return response
    
    def transcribe_audio_file(
        self,
        file_path: str | Path,
        language: str = None
    ) -> dict:
        """
        Transcribe audio file from filesystem.
        
        Args:
            file_path: Path to audio file
            language: Language code (default: None for auto-detection)
        
        Returns:
            Dictionary containing transcription and metadata
        """
        with open(file_path, "rb") as audio_file:
            return self.transcribe_audio(audio_file, language=language)
    
    def get_average_confidence(self, transcription: dict) -> Optional[float]:
        """
        Calculate average confidence from Whisper segments.
        
        Note: Whisper doesn't provide explicit confidence scores in the current API,
        but we can use segment-level no_speech_prob as a proxy.
        
        Args:
            transcription: Transcription dict from transcribe_audio
        
        Returns:
            Average confidence score (0-1) or None if not available
        """
        segments = transcription.get("segments", [])
        if not segments:
            return None
        
        # Use inverse of no_speech_prob as confidence proxy
        confidences = [
            1.0 - seg.get("no_speech_prob", 0.0)
            for seg in segments
            if "no_speech_prob" in seg
        ]
        
        if not confidences:
            return None
        
        return sum(confidences) / len(confidences)


# Global service instance
_asr_service: Optional[ASRService] = None


def get_asr_service() -> ASRService:
    """Get global ASR service instance (singleton pattern)"""
    global _asr_service
    if _asr_service is None:
        _asr_service = ASRService()
    return _asr_service

