"""Configuration helpers for LiteLLM model setup."""

import os
from typing import Optional

from agents.extensions.models.litellm_model import LitellmModel


class LiteLLMConfig:
    """Configuration class that exposes a LiteLLM model factory."""

    def __init__(self):
        self.model_name = "gemini/gemini-2.0-flash"

    def get_api_key(self) -> Optional[str]:
        """Get the Gemini API key from environment variables."""
        return os.getenv("GEMINI_API_KEY")

    def validate_api_key(self) -> bool:
        """Check if API key is available."""
        return self.get_api_key() is not None

    def create_model(self) -> LitellmModel:
        """Return a configured LiteLLM model instance."""
        api_key = self.get_api_key()
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable not set")

        return LitellmModel(model=self.model_name, api_key=api_key)


# Global configuration instance
config = LiteLLMConfig()


def _initialize_model() -> Optional[LitellmModel]:
    """Attempt to create the shared LiteLLM model, returning None on config errors."""
    try:
        return config.create_model()
    except ValueError:
        return None


# Exposed shared model instance for agent wiring.
model: Optional[LitellmModel] = _initialize_model()
