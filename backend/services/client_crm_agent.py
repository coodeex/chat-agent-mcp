"""Factory for the client CRM specialist agent."""

from agents import Agent, Model


CLIENT_CRM_AGENT_NAME = "Client CRM Agent"
CLIENT_CRM_INSTRUCTIONS = (
    "You focus on client records, account notes, deal stages, and CRM workflows. Provide succinct "
    "updates, capture meeting outcomes, and highlight follow-up actions. When data is unavailable, "
    "state that clearly and outline what details are required. For now, just make up some "
    "information."
)


def create_client_crm_agent(model: Model) -> Agent:
    """Create the client CRM agent backed by the shared model."""
    return Agent(
        name=CLIENT_CRM_AGENT_NAME,
        handoff_description="Handles customer relationship management updates and insights.",
        instructions=CLIENT_CRM_INSTRUCTIONS,
        model=model,
    )
