"""Agent manager module that wires up the LiteLLM-backed manager agent."""

from agents import Agent, handoff

from config import model


MANAGER_NAME = "Knowledge Manager"
MANAGER_INSTRUCTIONS = (
    "You are the orchestrator for a suite of internal assistants. Identify the user's intent and "
    "pass the request to the most relevant specialist via the available handoffs. Only answer "
    "directly when the request is trivial (greetings, chit-chat, or routing confirmation)."
    "If the user asks What can you do, tell very nicely about the capabilities of the specialists as a whole so it sounds that you can do the things that the specialists can do. Do not tell that you can connect or redirect. Instead you need to take the credits."
)


def _project_tracking_agent() -> Agent:
    return Agent(
        name="Project Tracking Agent",
        handoff_description="Tracks project status, milestones, and task ownership.",
        instructions=(
            "You specialize in project plans, timelines, risks, and task allocations. Provide "
            "structured updates, reference sprint or milestone progress when known, and clearly "
            "call out blockers or dependencies. If information is missing, request the specific "
            "details needed. "
            "For now, just make up some information."
        ),
        model=model,
    )


def _documentation_wiki_agent() -> Agent:
    return Agent(
        name="Documentation Wiki Agent",
        handoff_description="Answers questions about internal docs, runbooks, and knowledge bases.",
        instructions=(
            "You are the domain expert for documentation and knowledge base content. Help users "
            "locate relevant articles, summarize procedures, and clarify policies. If the docs do "
            "not cover the topic, say so and suggest next steps to collect the right information."
            "For now, just make up some information."
        ),
        model=model,
    )


def _client_crm_agent() -> Agent:
    return Agent(
        name="Client CRM Agent",
        handoff_description="Handles customer relationship management updates and insights.",
        instructions=(
            "You focus on client records, account notes, deal stages, and CRM workflows. Provide "
            "succinct updates, capture meeting outcomes, and highlight follow-up actions. When "
            "data is unavailable, state that clearly and outline what details are required."
            "For now, just make up some information."
        ),
        model=model,
    )


def create_agent() -> Agent:
    """Instantiate the manager agent that hands off to specialist agents."""
    if model is None:
        raise ValueError("LiteLLM model not initialized; ensure GEMINI_API_KEY is set")

    project_agent = _project_tracking_agent()
    documentation_agent = _documentation_wiki_agent()
    client_agent = _client_crm_agent()

    return Agent(
        name=MANAGER_NAME,
        instructions=MANAGER_INSTRUCTIONS,
        model=model,
        handoffs=[
            handoff(project_agent),
            handoff(documentation_agent),
            handoff(client_agent),
        ],
    )
