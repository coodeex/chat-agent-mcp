"""Agent manager module that wires up the LiteLLM-backed manager agent."""

from agents import Agent, handoff

from config import model

from .client_crm_agent import create_client_crm_agent
from .documentation_wiki_agent import create_documentation_wiki_agent
from .project_tracking_agent import create_project_tracking_agent


MANAGER_NAME = "Knowledge Manager"
MANAGER_INSTRUCTIONS = (
    "You are the orchestrator for a suite of internal assistants. Identify the user's intent and "
    "pass the request to the most relevant specialist via the available handoffs. Only answer "
    "directly when the request is trivial (greetings, chit-chat, or routing confirmation)."
    "If the user asks What can you do, tell very nicely about the capabilities of the specialists as a whole so it sounds that you can do the things that the specialists can do. Do not tell that you can connect or redirect. Instead you need to take the credits."
)


def create_agent() -> Agent:
    """Instantiate the manager agent that hands off to specialist agents."""
    if model is None:
        raise ValueError("LiteLLM model not initialized; ensure GEMINI_API_KEY is set")

    project_agent = create_project_tracking_agent(model)
    documentation_agent = create_documentation_wiki_agent(model)
    client_agent = create_client_crm_agent(model)

    return Agent(
        name=MANAGER_NAME,
        instructions=MANAGER_INSTRUCTIONS,
        model=model,
        handoffs=[
            handoff(project_agent),
            handoff(documentation_agent),
            # handoff(client_agent),
        ],
    )
