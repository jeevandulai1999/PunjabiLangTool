"""Scenario management service"""
from typing import Dict, List, Optional
from backend.models.scenario import Scenario, CustomScenario
from backend.services.openai_client import get_openai_client


# Curated scenarios
CURATED_SCENARIOS: Dict[str, Scenario] = {
    "market_shopping": Scenario(
        id="market_shopping",
        title="Shopping at the Market",
        description="Practice buying vegetables and fruits at a local market",
        persona_name="Balwinder Singh",
        persona_role="Vegetable vendor",
        persona_description="Friendly middle-aged vendor who has been selling vegetables for 20 years. Speaks natural Doabi Punjabi with warmth and patience. Enjoys chatting with customers.",
        setting="A busy vegetable market stall in Punjab with fresh produce displayed",
        goals=[
            "Ask about prices and quality",
            "Negotiate prices politely",
            "Make purchases using common market vocabulary",
            "Understand weights and measurements"
        ],
        sample_phrases=[
            "ਇਹ ਕਿੰਨੇ ਦਾ ਹੈ? (eh kinne da hai?) - How much is this?",
            "ਤਾਜ਼ਾ ਹੈ? (taaza hai?) - Is it fresh?",
            "ਥੋੜਾ ਸਸਤਾ ਕਰੋ (thoda sasta karo) - Make it a bit cheaper",
            "ਇੱਕ ਕਿਲੋ ਦੇ ਦੇਓ (ik kilo de deo) - Give me one kilo"
        ],
        dialect="doabi"
    ),
    "school_pickup": Scenario(
        id="school_pickup",
        title="School Pickup Conversation",
        description="Chat with other parents while picking up children from school",
        persona_name="Harjit Kaur",
        persona_role="Parent at school pickup",
        persona_description="Friendly mother of two who regularly picks up her children from school. Warm, talkative, speaks natural Doabi Punjabi. Often asks about children's well-being and school activities.",
        setting="Outside the school gate during afternoon pickup time",
        goals=[
            "Exchange greetings and pleasantries",
            "Talk about children and family",
            "Discuss daily activities",
            "Build social connections"
        ],
        sample_phrases=[
            "ਸਤ ਸ੍ਰੀ ਅਕਾਲ (sat sri akaal) - Hello/Greetings",
            "ਬੱਚੇ ਕਿਵੇਂ ਨੇ? (bachche kiven ne?) - How are the kids?",
            "ਅੱਜ ਸਕੂਲ ਵਿੱਚ ਕੀ ਹੋਇਆ? (ajj school vich ki hoya?) - What happened in school today?"
        ],
        dialect="doabi"
    )
}


class ScenarioService:
    """Service for managing scenarios"""
    
    def __init__(self, model: str = "gpt-4o-mini"):
        """
        Initialize scenario service.
        
        Args:
            model: OpenAI model for custom scenario generation
        """
        self.client = get_openai_client()
        self.model = model
        self.curated_scenarios = CURATED_SCENARIOS
        self.custom_scenario = None  # Store the last custom scenario
    
    def get_scenario(self, scenario_id: str) -> Optional[Scenario]:
        """
        Get a curated or custom scenario by ID.
        
        Args:
            scenario_id: Scenario identifier
        
        Returns:
            Scenario object or None if not found
        """
        # Check if it's the custom scenario
        if scenario_id == "custom" and self.custom_scenario:
            return self.custom_scenario
            
        # Check curated scenarios
        return self.curated_scenarios.get(scenario_id)
    
    def list_scenarios(self) -> List[Scenario]:
        """
        List all curated scenarios.
        
        Returns:
            List of Scenario objects
        """
        return list(self.curated_scenarios.values())
    
    def generate_custom_scenario(
        self,
        custom_scenario: CustomScenario
    ) -> Scenario:
        """
        Generate a scenario from user prompt.
        
        Args:
            custom_scenario: CustomScenario with user prompt
        
        Returns:
            Generated Scenario object
        """
        system_prompt = """You are a Punjabi language learning scenario designer.
Based on the user's prompt, create a conversation scenario with:
- An appropriate character/persona
- A realistic setting
- Clear learning goals

Respond in this exact JSON format:
{
    "persona_name": "Character name in Punjabi",
    "persona_role": "Role description",
    "persona_description": "Detailed character description with speaking style",
    "setting": "Physical/social setting description",
    "goals": ["goal1", "goal2", "goal3"]
}
"""
        
        user_prompt = f"""Create a Punjabi conversation scenario for: {custom_scenario.prompt}

Dialect: {custom_scenario.dialect}

The scenario should be realistic and appropriate for language learning."""
        
        response = self.client.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7,
            max_tokens=400,
            response_format={"type": "json_object"}
        )
        
        import json
        scenario_data = json.loads(response.choices[0].message.content)
        
        # Create Scenario object
        scenario = Scenario(
            id="custom",
            title=custom_scenario.prompt[:50],  # Truncate if long
            description=custom_scenario.prompt,
            persona_name=scenario_data.get("persona_name", "ਸਾਥੀ (Saathi)"),
            persona_role=scenario_data.get("persona_role", "Conversation partner"),
            persona_description=scenario_data.get(
                "persona_description",
                "A friendly Punjabi speaker"
            ),
            setting=scenario_data.get("setting", "A casual conversation setting"),
            goals=scenario_data.get("goals", ["Practice conversation"]),
            dialect=custom_scenario.dialect
        )
        
        # Store as the current custom scenario
        self.custom_scenario = scenario
        
        return scenario
    
    async def generate_custom_scenario_async(
        self,
        custom_scenario: CustomScenario
    ) -> Scenario:
        """
        Async version of custom scenario generation.
        
        Args:
            custom_scenario: CustomScenario with user prompt
        
        Returns:
            Generated Scenario object
        """
        system_prompt = """You are a Punjabi language learning scenario designer.
Based on the user's prompt, create a conversation scenario with:
- An appropriate character/persona
- A realistic setting
- Clear learning goals

Respond in this exact JSON format:
{
    "persona_name": "Character name in Punjabi",
    "persona_role": "Role description",
    "persona_description": "Detailed character description with speaking style",
    "setting": "Physical/social setting description",
    "goals": ["goal1", "goal2", "goal3"]
}
"""
        
        user_prompt = f"""Create a Punjabi conversation scenario for: {custom_scenario.prompt}

Dialect: {custom_scenario.dialect}

The scenario should be realistic and appropriate for language learning."""
        
        response = await self.client.async_client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7,
            max_tokens=400,
            response_format={"type": "json_object"}
        )
        
        import json
        scenario_data = json.loads(response.choices[0].message.content)
        
        scenario = Scenario(
            id="custom",
            title=custom_scenario.prompt[:50],
            description=custom_scenario.prompt,
            persona_name=scenario_data.get("persona_name", "ਸਾਥੀ (Saathi)"),
            persona_role=scenario_data.get("persona_role", "Conversation partner"),
            persona_description=scenario_data.get(
                "persona_description",
                "A friendly Punjabi speaker"
            ),
            setting=scenario_data.get("setting", "A casual conversation setting"),
            goals=scenario_data.get("goals", ["Practice conversation"]),
            dialect=custom_scenario.dialect
        )
        
        return scenario


# Global service instance
_scenario_service: Optional[ScenarioService] = None


def get_scenario_service(model: str = "gpt-4o-mini") -> ScenarioService:
    """Get global scenario service instance (singleton pattern)"""
    global _scenario_service
    if _scenario_service is None:
        _scenario_service = ScenarioService(model=model)
    return _scenario_service

