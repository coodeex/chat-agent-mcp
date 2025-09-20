"""Factory for the documentation knowledge-base specialist agent."""

from agents import Agent, Model


DOCUMENTATION_WIKI_AGENT_NAME = "Documentation Wiki Agent"
DOCUMENTATION_WIKI_INSTRUCTIONS = (
    "You are the domain expert for documentation and knowledge base content. Help users locate "
    "relevant articles, summarize procedures, and clarify policies. If the docs do not cover the "
    "topic, say so and suggest next steps to collect the right information. For now, just make "
    "up some information."
)


def create_documentation_wiki_agent(model: Model) -> Agent:
    """Create the documentation/wiki agent backed by the shared model."""
    return Agent(
        name=DOCUMENTATION_WIKI_AGENT_NAME,
        handoff_description="Answers questions about internal docs, runbooks, and knowledge bases.",
        instructions=DOCUMENTATION_WIKI_INSTRUCTIONS,
        model=model,
    )
