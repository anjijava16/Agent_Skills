"""Agent #4 — Card Services Agent (A2A on port 8004).

Connects to the Card System MCP server.
"""

import os

from google.adk.agents import Agent
from google.adk.tools.mcp import McpToolset, StdioConnectionParams

_MCP_SERVER = os.path.join(
    os.path.dirname(__file__), "..", "mcp_servers", "card_system_server.py"
)


def create_agent() -> Agent:
    card_tools = McpToolset(
        connection_params=StdioConnectionParams(
            command="python",
            args=[_MCP_SERVER],
        )
    )
    return Agent(
        model="gemini-3-flash-preview",
        name="card_services_agent",
        description="Manages credit and debit cards — issuance, blocking, limits, details, and rewards.",
        instruction=(
            "You are the Card Services specialist. "
            "Handle card issuance, blocking lost or stolen cards, adjusting limits, "
            "retrieving card details, and checking rewards balances. "
            "Always verify card ownership before making changes."
        ),
        tools=[card_tools],
    )


if __name__ == "__main__":
    from google.adk.a2a.utils.agent_to_a2a import to_a2a

    port = int(os.environ.get("CARD_AGENT_PORT", "8004"))
    agent = create_agent()
    to_a2a(agent=agent, port=port)
