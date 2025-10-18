"""Help Mode assistant service for grammar, vocabulary, culture, and alternatives"""
from typing import Optional, Dict, Any
from backend.services.openai_client import get_openai_client


class HelpService:
    """Service for providing help with grammar, vocabulary, culture, and alternatives"""
    
    def __init__(self, model: str = "gpt-4o-mini"):
        """
        Initialize help service.
        
        Args:
            model: OpenAI model to use
        """
        self.client = get_openai_client()
        self.model = model
    
    def _build_system_prompt(self, topic: Optional[str] = None) -> str:
        """
        Build system prompt for help assistant.
        
        Args:
            topic: Optional specific topic (grammar, vocabulary, culture, alternatives)
        
        Returns:
            System prompt string
        """
        base_prompt = """You are a helpful Punjabi language learning assistant specializing in Doabi dialect.

Your role is to provide clear, concise explanations about:
- Grammar rules and sentence structure
- Vocabulary meanings and usage
- Cultural context and appropriate expressions
- Alternative phrasings (more polite, simpler, more formal/informal)

Guidelines:
- Keep explanations simple and practical
- Provide examples in Gurmukhi script, Romanised Punjabi, and English
- Be encouraging and supportive
- Focus on conversational, everyday usage
- If relevant, mention cultural nuances"""
        
        if topic:
            topic_guidance = {
                "grammar": "Focus on explaining grammatical structures, verb conjugations, and sentence patterns.",
                "vocabulary": "Focus on word meanings, synonyms, usage contexts, and related words.",
                "culture": "Focus on cultural context, appropriate situations, formality levels, and social norms.",
                "alternatives": "Focus on providing different ways to express the same idea with varying politeness, formality, or simplicity."
            }
            
            if topic in topic_guidance:
                base_prompt += f"\n\nCurrent focus: {topic_guidance[topic]}"
        
        return base_prompt
    
    def get_help(
        self,
        query: str,
        context: Optional[str] = None,
        topic: Optional[str] = None
    ) -> str:
        """
        Get help response for user query.
        
        Args:
            query: User's help question
            context: Optional conversation context
            topic: Optional topic category (grammar, vocabulary, culture, alternatives)
        
        Returns:
            Help response with examples
        """
        system_prompt = self._build_system_prompt(topic)
        
        user_prompt = f"Question: {query}"
        
        if context:
            user_prompt += f"\n\nConversation context: {context}"
        
        response = self.client.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.5,  # Moderate temperature for helpful but consistent responses
            max_tokens=500  # Allow longer explanations
        )
        
        help_text = response.choices[0].message.content
        return help_text.strip() if help_text else ""
    
    async def get_help_async(
        self,
        query: str,
        context: Optional[str] = None,
        topic: Optional[str] = None
    ) -> str:
        """
        Async version of help response.
        
        Args:
            query: User's help question
            context: Optional conversation context
            topic: Optional topic category
        
        Returns:
            Help response with examples
        """
        system_prompt = self._build_system_prompt(topic)
        
        user_prompt = f"Question: {query}"
        
        if context:
            user_prompt += f"\n\nConversation context: {context}"
        
        response = await self.client.async_client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.5,
            max_tokens=500
        )
        
        help_text = response.choices[0].message.content
        return help_text.strip() if help_text else ""
    
    def suggest_alternatives(
        self,
        punjabi_text: str,
        context: Optional[str] = None
    ) -> Dict[str, str]:
        """
        Suggest alternative phrasings for given Punjabi text.
        
        Args:
            punjabi_text: Punjabi text to provide alternatives for
            context: Optional context
        
        Returns:
            Dictionary with alternative phrasings (polite, simple, formal, informal)
        """
        system_prompt = self._build_system_prompt("alternatives")
        
        user_prompt = f"""Provide alternative ways to say this in Punjabi:
{punjabi_text}

Please provide:
1. More polite version
2. Simpler/more casual version
3. More formal version (if different from polite)

Format each as: [Category]: [Gurmukhi] ([Romanised]) - [English meaning]"""
        
        if context:
            user_prompt += f"\n\nContext: {context}"
        
        response = self.client.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.6,
            max_tokens=400
        )
        
        alternatives_text = response.choices[0].message.content
        
        # Return as formatted text for now; could parse into structured dict if needed
        return {"alternatives": alternatives_text.strip() if alternatives_text else ""}


# Global service instance
_help_service: Optional[HelpService] = None


def get_help_service(model: str = "gpt-4o-mini") -> HelpService:
    """Get global help service instance (singleton pattern)"""
    global _help_service
    if _help_service is None:
        _help_service = HelpService(model=model)
    return _help_service

