"""Scenario data models"""
from typing import List, Optional
from pydantic import BaseModel, Field


class Scenario(BaseModel):
    """Represents a conversation scenario"""
    
    id: str = Field(description="Unique scenario identifier")
    title: str = Field(description="Scenario title")
    description: str = Field(description="Brief description of the scenario")
    persona_name: str = Field(description="Name of the AI character")
    persona_role: str = Field(description="Role of the AI character (e.g., shopkeeper, teacher)")
    persona_description: str = Field(description="Character description and behavior guidelines")
    setting: str = Field(description="Physical/social setting of the scenario")
    goals: List[str] = Field(description="Learning goals for this scenario")
    sample_phrases: Optional[List[str]] = Field(
        default=None,
        description="Sample phrases user might need"
    )
    dialect: str = Field(default="doabi", description="Punjabi dialect to use")
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": "market_shopping",
                "title": "Shopping at the Market",
                "description": "Practice buying vegetables at a local market",
                "persona_name": "Balwinder Singh",
                "persona_role": "Vegetable vendor",
                "persona_description": "Friendly middle-aged vendor who speaks Doabi Punjabi naturally",
                "setting": "A busy vegetable market stall in Punjab",
                "goals": ["Negotiate prices", "Ask about produce", "Make purchases"],
                "sample_phrases": ["ਇਹ ਕਿੰਨੇ ਦਾ ਹੈ? (eh kinne da hai?)", "How much is this?"],
                "dialect": "doabi"
            }
        }


class CustomScenario(BaseModel):
    """User-generated custom scenario"""
    
    prompt: str = Field(description="User's scenario description/prompt")
    dialect: str = Field(default="doabi", description="Punjabi dialect to use")

