"""
Configuration file for LiteLLM model setup and agent configuration.
"""

import os
from typing import List, Optional
from agents import Agent, function_tool
from agents.extensions.models.litellm_model import LitellmModel


# ---------- Function tools ----------
@function_tool
def get_weather(city: str):
    """Get weather information for a city."""
    print(f"[debug] getting weather for {city}")
    return f"The weather in {city} is sunny with 22°C."


@function_tool
def calculate(expression: str):
    """Calculate a mathematical expression safely."""
    try:
        # Simple safe evaluation for basic math
        result = eval(expression, {"__builtins__": {}}, {})
        return f"The result of {expression} is {result}"
    except Exception as e:
        return f"Cannot calculate {expression}: {str(e)}"


class LiteLLMConfig:
    """Configuration class for LiteLLM model and agent setup."""
    
    def __init__(self):
        self.model_name = "gemini/gemini-2.0-flash"
        self.agent_name = "Gemini Assistant"
        self.agent_instructions = "You are a helpful and concise assistant. You can help with weather information and calculations."
        self.tools = [get_weather, calculate]
    
    def get_api_key(self) -> Optional[str]:
        """Get the Gemini API key from environment variables."""
        return os.getenv("GEMINI_API_KEY")
    
    def validate_api_key(self) -> bool:
        """Check if API key is available."""
        return self.get_api_key() is not None
    
    def create_agent(self) -> Agent:
        """Create and return a configured Agent instance."""
        api_key = self.get_api_key()
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable not set")
        
        return Agent(
            name=self.agent_name,
            instructions=self.agent_instructions,
            model=LitellmModel(model=self.model_name, api_key=api_key),
            tools=self.tools,
        )


# Global configuration instance
config = LiteLLMConfig()
