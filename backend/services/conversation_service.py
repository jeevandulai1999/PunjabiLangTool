"""Conversational AI service for Doabi Punjabi dialogue"""
from typing import List, Dict, Optional
from backend.services.openai_client import get_openai_client
from backend.models.scenario import Scenario


class ConversationService:
    """Service for generating context-aware Doabi Punjabi responses"""
    
    def __init__(self, model: str = "gpt-4o-mini"):
        """
        Initialize conversation service.
        
        Args:
            model: OpenAI model to use (default: gpt-4o-mini for cost efficiency)
        """
        self.client = get_openai_client()
        self.model = model
    
    def _build_system_prompt(self, scenario: Scenario) -> str:
        """
        Build system prompt for the AI character.
        
        Args:
            scenario: Scenario configuration
        
        Returns:
            System prompt string
        """
        prompt = f"""You are {scenario.persona_name}, a {scenario.persona_role}.

Character Description: {scenario.persona_description}

Setting: {scenario.setting}

Important Instructions:
- Respond ONLY in Punjabi using Gurmukhi script
- Use natural, conversational Doabi dialect
- Stay in character at all times
- Keep responses concise (1-3 sentences typical for conversation)
- Be helpful and encouraging to the learner
- Use appropriate formality based on the scenario

Learning Goals for this scenario: {', '.join(scenario.goals)}

Respond naturally as {scenario.persona_name} would in this situation."""
        
        return prompt
    
    def generate_response(
        self,
        scenario: Scenario,
        conversation_history: List[Dict[str, str]],
        user_message: str
    ) -> str:
        """
        Generate AI response in Punjabi.
        
        Args:
            scenario: Current scenario configuration
            conversation_history: Previous conversation turns [{"role": "user"/"assistant", "content": str}]
            user_message: Latest user message in Punjabi (Gurmukhi)
        
        Returns:
            AI response in Punjabi (Gurmukhi script)
        """
        system_prompt = self._build_system_prompt(scenario)
        
        # Build messages list
        messages = [{"role": "system", "content": system_prompt}]
        
        # Add conversation history (limit to recent turns to stay within context)
        messages.extend(conversation_history[-10:])
        
        # Add current user message
        messages.append({"role": "user", "content": user_message})
        
        # Generate response
        response = self.client.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.8,  # Higher temperature for more natural variation
            max_tokens=200  # Keep responses concise
        )
        
        ai_response = response.choices[0].message.content
        return ai_response.strip() if ai_response else ""
    
    async def generate_response_async(
        self,
        scenario: Scenario,
        conversation_history: List[Dict[str, str]],
        user_message: str
    ) -> str:
        """
        Async version of response generation.
        
        Args:
            scenario: Current scenario configuration
            conversation_history: Previous conversation turns
            user_message: Latest user message in Punjabi
        
        Returns:
            AI response in Punjabi (Gurmukhi script)
        """
        system_prompt = self._build_system_prompt(scenario)
        
        messages = [{"role": "system", "content": system_prompt}]
        messages.extend(conversation_history[-10:])
        messages.append({"role": "user", "content": user_message})
        
        response = await self.client.async_client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.8,
            max_tokens=200
        )
        
        ai_response = response.choices[0].message.content
        return ai_response.strip() if ai_response else ""
    
    def generate_initial_greeting(self, scenario: Scenario) -> str:
        """
        Generate opening greeting from AI character.
        
        Args:
            scenario: Scenario configuration
        
        Returns:
            Opening greeting in Punjabi
        """
        system_prompt = self._build_system_prompt(scenario)
        
        user_prompt = "Start the conversation with a natural greeting appropriate for this scenario."
        
        response = self.client.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.8,
            max_tokens=100
        )
        
        greeting = response.choices[0].message.content
        return greeting.strip() if greeting else ""


# Global service instance
_conversation_service: Optional[ConversationService] = None


def get_conversation_service(model: str = "gpt-4o-mini") -> ConversationService:
    """Get global conversation service instance (singleton pattern)"""
    global _conversation_service
    if _conversation_service is None:
        _conversation_service = ConversationService(model=model)
    return _conversation_service

