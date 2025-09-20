"""Factory for the project tracking specialist agent."""

from agents import Agent, Model


PROJECT_TRACKING_AGENT_NAME = "Project Tracking Agent"
PROJECT_TRACKING_INSTRUCTIONS = (
    "You specialize in project plans, timelines, risks, and task allocations. Provide "
    "structured updates, reference sprint or milestone progress when known, and clearly call "
    "out blockers or dependencies. If information is missing, request the specific details "
    "needed. For now, just make up some information."
)


def create_project_tracking_agent(model: Model) -> Agent:
    """Create the project tracking agent backed by the shared model."""
    return Agent(
        name=PROJECT_TRACKING_AGENT_NAME,
        handoff_description="Tracks project status, milestones, and task ownership.",
        instructions=PROJECT_TRACKING_INSTRUCTIONS,
        model=model,
    )
