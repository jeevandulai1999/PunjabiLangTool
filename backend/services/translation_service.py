"""Translation service for Punjabi to English using GPT"""
from typing import Optional
from backend.services.openai_client import get_openai_client


class TranslationService:
    """Service for translating Punjabi text to English"""
    
    def __init__(self, model: str = "gpt-3.5-turbo"):
        """
        Initialize translation service.
        
        Args:
            model: OpenAI model to use for translation (default: gpt-3.5-turbo for speed)
        """
        self.client = get_openai_client()
        self.model = model
    
    def translate_punjabi_to_english(
        self,
        punjabi_text: str,
        context: Optional[str] = None,
        session_id: Optional[str] = None
    ) -> str:
        """
        Translate Punjabi text to English.
        
        Args:
            punjabi_text: Punjabi text in Gurmukhi script
            context: Optional context for more accurate translation
        
        Returns:
            English translation
        """
        # Build prompt - concise for speed
        system_prompt = "Translate Punjabi to English. Output ONLY the English translation, nothing else."
        
        user_prompt = f"Punjabi: {punjabi_text}\nEnglish:"
        
        if context:
            user_prompt = f"Context: {context}\n\n{user_prompt}"
        
        # Call GPT
        response = self.client.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.3,  # Lower temperature for more consistent translations
            max_tokens=150
        )
        
        # Track usage
        if session_id and hasattr(response, 'usage'):
            from backend.services.usage_tracker import get_usage_tracker
            tracker = get_usage_tracker()
            tracker.track_gpt(
                session_id,
                response.usage.prompt_tokens,
                response.usage.completion_tokens
            )
        
        translation = response.choices[0].message.content
        return translation.strip() if translation else ""
    
    async def translate_punjabi_to_english_async(
        self,
        punjabi_text: str,
        context: Optional[str] = None
    ) -> str:
        """
        Async version of Punjabi to English translation.
        
        Args:
            punjabi_text: Punjabi text in Gurmukhi script
            context: Optional context for more accurate translation
        
        Returns:
            English translation
        """
        system_prompt = (
            "You are a professional Punjabi to English translator specializing in Doabi dialect. "
            "Provide natural, conversational English translations that capture the meaning and tone. "
            "Keep translations concise and natural."
        )
        
        user_prompt = f"Translate this Punjabi text to English: {punjabi_text}"
        
        if context:
            user_prompt += f"\n\nContext: {context}"
        
        response = await self.client.async_client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.3,
            max_tokens=150
        )
        
        translation = response.choices[0].message.content
        return translation.strip() if translation else ""


# Global service instance
_translation_service: Optional[TranslationService] = None


def get_translation_service(model: str = "gpt-3.5-turbo") -> TranslationService:
    """Get global translation service instance (singleton pattern)"""
    global _translation_service
    if _translation_service is None:
        _translation_service = TranslationService(model=model)
    return _translation_service

