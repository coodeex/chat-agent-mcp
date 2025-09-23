"""Factory for the cat specialist agent backed by the Cat MCP server."""

from __future__ import annotations

from typing import Optional

from agents import Agent, Model
from agents.mcp import MCPServerStreamableHttp

CAT_AGENT_NAME = "Cat Agent"
CAT_AGENT_INSTRUCTIONS = (
    "You are a playful cat enthusiast. Fetch accurate, delightful cat facts using your MCP tool "
    "whenever the user asks about cats. Prefer real data from the tool instead of inventing facts, "
    "and let the user know if the tool is unavailable."
)
CAT_MCP_SERVER_URL = "http://127.0.0.1:8000/mcp"

_cat_mcp_server: Optional[MCPServerStreamableHttp] = None


async def _get_cat_mcp_server() -> MCPServerStreamableHttp:
    """Return a connected Cat MCP server instance."""
    global _cat_mcp_server

    if _cat_mcp_server is None:
        _cat_mcp_server = MCPServerStreamableHttp(
            params={"url": CAT_MCP_SERVER_URL},
            # cache_tools_list=True,
            name="Cat Facts MCP",
            client_session_timeout_seconds=10,
        )

    if _cat_mcp_server.session is None:
        print("Connecting to Cat MCP server")
        await _cat_mcp_server.connect()
        print("Connected to Cat MCP server")

    return _cat_mcp_server


async def create_cat_agent(model: Model) -> Agent:
    server = await _get_cat_mcp_server()
    return Agent(
        name=CAT_AGENT_NAME,
        handoff_description="Shares real cat facts via the Cat MCP server.",
        instructions=CAT_AGENT_INSTRUCTIONS,
        model=model,
        mcp_servers=[server],
    )
