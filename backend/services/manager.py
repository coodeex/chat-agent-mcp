"""Agent manager module that wires up tools and the LiteLLM model."""

from agents import Agent, function_tool

from config import config, model


AGENT_NAME = "Gemini Assistant"
AGENT_INSTRUCTIONS = (
    "You are a helpful and concise assistant. You can help with weather information and "
    "calculations."
)


@function_tool
def get_weather(city: str):
    """Get weather information for a city."""
    print(f"[debug] getting weather for {city}")
    return f"The weather in {city} is sunny with 22°C."


@function_tool
def calculate(expression: str):
    """Calculate a mathematical expression safely."""
    try:
        # Guarded eval for simple math expressions only.
        result = eval(expression, {"__builtins__": {}}, {})
        return f"The result of {expression} is {result}"
    except Exception as exc:
        return f"Cannot calculate {expression}: {exc}"


def create_agent() -> Agent:
    """Instantiate the default agent using the shared LiteLLM model."""
    if model is None:
        raise ValueError("LiteLLM model not initialized; ensure GEMINI_API_KEY is set")
    return Agent(
        name=AGENT_NAME,
        instructions=AGENT_INSTRUCTIONS,
        model=model,
        tools=[get_weather, calculate],
    )
