"""Orchestrator service to coordinate all services for a complete conversation flow"""
from typing import BinaryIO, Optional, Dict
from pathlib import Path
import time

from backend.models.transcript import TriScript, TranscriptWithConfidence
from backend.models.scenario import Scenario, CustomScenario
from backend.services.asr_service import get_asr_service
from backend.services.transliteration import transliterate_gurmukhi_to_roman
from backend.services.translation_service import get_translation_service
from backend.services.conversation_service import get_conversation_service
from backend.services.tts_service import get_tts_service
from backend.services.help_service import get_help_service
from backend.services.scenario_service import get_scenario_service
from backend.services.session_manager import SessionManager


class ConversationOrchestrator:
    """Orchestrates the complete conversation flow"""
    
    def __init__(self):
        """Initialize orchestrator with all services"""
        self.asr_service = get_asr_service()
        self.translation_service = get_translation_service()
        self.conversation_service = get_conversation_service()
        self.tts_service = get_tts_service()
        self.help_service = get_help_service()
        self.scenario_service = get_scenario_service()
    
    def process_user_audio(
        self,
        audio_file: BinaryIO,
        session: SessionManager
    ) -> TranscriptWithConfidence:
        """
        Process user audio through complete pipeline:
        Audio -> ASR -> Gurmukhi -> Romanised -> English
        
        Args:
            audio_file: Audio file in binary mode
            session: Session manager
        
        Returns:
            TranscriptWithConfidence with all three scripts
        """
        try:
            # Step 1: ASR - transcribe audio (Whisper auto-detects Punjabi)
            print("DEBUG: Starting ASR transcription...")
            transcription = self.asr_service.transcribe_audio(audio_file)
            print(f"DEBUG: ASR completed, got: {transcription.get('text', '')[:50]}...")
            print(f"DEBUG: Detected language: {transcription.get('language', 'unknown')}")
        except Exception as e:
            print(f"ERROR in ASR: {str(e)}")
            raise
        gurmukhi_text = transcription.get("text", "")
        
        # Step 2: Calculate confidence
        confidence = self.asr_service.get_average_confidence(transcription)
        duration = transcription.get("duration", 0.0)
        
        # Step 3: Transliterate to Romanised Punjabi
        romanised_text = transliterate_gurmukhi_to_roman(gurmukhi_text)
        
        # Step 4: Translate to English
        english_text = self.translation_service.translate_punjabi_to_english(
            gurmukhi_text,
            context=session.get_recent_context(num_turns=3)
        )
        
        return TranscriptWithConfidence(
            gurmukhi=gurmukhi_text,
            romanised=romanised_text,
            english=english_text,
            confidence=confidence,
            duration_seconds=duration
        )
    
    def generate_ai_response(
        self,
        user_transcript: TriScript,
        session: SessionManager,
        audio_output_path: Optional[str] = None
    ) -> Dict[str, any]:
        """
        Generate AI response with audio and tri-script.
        
        Args:
            user_transcript: User's tri-script transcript
            session: Session manager
            audio_output_path: Optional path to save audio
        
        Returns:
            Dictionary with transcript and audio_path
        """
        # Step 1: Generate Punjabi response
        ai_response_gurmukhi = self.conversation_service.generate_response(
            scenario=session.scenario,
            conversation_history=session.conversation_history,
            user_message=user_transcript.gurmukhi
        )
        
        # Step 2: Transliterate to Romanised
        ai_response_romanised = transliterate_gurmukhi_to_roman(ai_response_gurmukhi)
        
        # Step 3: Translate to English
        ai_response_english = self.translation_service.translate_punjabi_to_english(
            ai_response_gurmukhi
        )
        
        # Step 4: Generate audio
        if audio_output_path is None:
            # Generate temp path
            audio_output_path = f"frontend/static/audio/{session.session_id}_{int(time.time())}.mp3"
        
        self.tts_service.generate_speech(
            text=ai_response_gurmukhi,
            output_path=audio_output_path
        )
        
        ai_transcript = TriScript(
            gurmukhi=ai_response_gurmukhi,
            romanised=ai_response_romanised,
            english=ai_response_english
        )
        
        return {
            "transcript": ai_transcript,
            "audio_path": audio_output_path
        }
    
    def process_conversation_turn(
        self,
        audio_file: BinaryIO,
        session: SessionManager,
        audio_output_dir: Optional[str] = None
    ) -> Dict[str, any]:
        """
        Process complete conversation turn: user audio -> AI response with audio.
        
        Args:
            audio_file: User audio file
            session: Session manager
            audio_output_dir: Optional directory for AI audio
        
        Returns:
            Dictionary with user_transcript, ai_transcript, ai_audio_path
        """
        # Process user audio
        user_transcript = self.process_user_audio(audio_file, session)
        
        # Add user turn to session
        session.add_turn(
            speaker="user",
            transcript=user_transcript,
            confidence=user_transcript.confidence
        )
        
        # Generate AI response
        audio_path = None
        if audio_output_dir:
            audio_path = f"{audio_output_dir}/{session.session_id}_{len(session.turns)}.mp3"
        
        ai_response = self.generate_ai_response(
            user_transcript,
            session,
            audio_output_path=audio_path
        )
        
        # Add AI turn to session
        session.add_turn(
            speaker="ai",
            transcript=ai_response["transcript"],
            audio_url=ai_response["audio_path"]
        )
        
        return {
            "user_transcript": user_transcript,
            "ai_transcript": ai_response["transcript"],
            "ai_audio_path": ai_response["audio_path"]
        }
    
    def get_help_response(
        self,
        query: str,
        session: SessionManager,
        topic: Optional[str] = None
    ) -> str:
        """
        Get help response for user query.
        
        Args:
            query: User's help question
            session: Session manager
            topic: Optional topic (grammar, vocabulary, culture, alternatives)
        
        Returns:
            Help response text
        """
        context = session.get_recent_context(num_turns=5)
        
        # Enter help mode
        session.enter_help_mode()
        
        # Get help
        help_response = self.help_service.get_help(
            query=query,
            context=context,
            topic=topic
        )
        
        # Exit help mode
        session.exit_help_mode()
        
        return help_response
    
    def start_scenario_greeting(
        self,
        session: SessionManager,
        audio_output_path: Optional[str] = None
    ) -> Dict[str, any]:
        """
        Generate initial greeting for scenario.
        
        Args:
            session: Session manager
            audio_output_path: Optional path for audio
        
        Returns:
            Dictionary with transcript and audio_path
        """
        # Generate greeting
        greeting_gurmukhi = self.conversation_service.generate_initial_greeting(
            session.scenario
        )
        
        # Transliterate and translate
        greeting_romanised = transliterate_gurmukhi_to_roman(greeting_gurmukhi)
        greeting_english = self.translation_service.translate_punjabi_to_english(
            greeting_gurmukhi
        )
        
        # Generate audio
        if audio_output_path is None:
            audio_output_path = f"frontend/static/audio/{session.session_id}_greeting.mp3"
        
        self.tts_service.generate_speech(
            text=greeting_gurmukhi,
            output_path=audio_output_path
        )
        
        greeting_transcript = TriScript(
            gurmukhi=greeting_gurmukhi,
            romanised=greeting_romanised,
            english=greeting_english
        )
        
        # Add to session
        session.add_turn(
            speaker="ai",
            transcript=greeting_transcript,
            audio_url=audio_output_path
        )
        
        return {
            "transcript": greeting_transcript,
            "audio_path": audio_output_path
        }


# Global orchestrator instance
_orchestrator: Optional[ConversationOrchestrator] = None


def get_orchestrator() -> ConversationOrchestrator:
    """Get global orchestrator instance (singleton pattern)"""
    global _orchestrator
    if _orchestrator is None:
        _orchestrator = ConversationOrchestrator()
    return _orchestrator

