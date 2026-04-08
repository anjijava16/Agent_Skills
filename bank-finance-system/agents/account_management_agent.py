"""Agent #1 — Account Management Agent (A2A on port 8001).

Connects to the Account DB MCP server and exposes account operations.
"""

import os
import sys

from google.adk.agents import Agent
from google.adk.tools.mcp import McpToolset, StdioConnectionParams

_MCP_SERVER = os.path.join(
    os.path.dirname(__file__), "..", "mcp_servers", "account_db_server.py"
)


def create_agent() -> Agent:
    """Create the account management agent with MCP tools."""
    account_tools = McpToolset(
        connection_params=StdioConnectionParams(
            command="python",
            args=[_MCP_SERVER],
        )
    )
    return Agent(
        model="gemini-3-flash-preview",
        name="account_management_agent",
        description="Manages bank accounts — create, read, update accounts and check balances.",
        instruction=(
            "You are the Account Management specialist at the bank. "
            "Use your tools to look up accounts, create new ones, update details, "
            "and check balances. Always confirm the account ID before making changes. "
            "Return structured information to the caller."
        ),
        tools=[account_tools],
    )


if __name__ == "__main__":
    from google.adk.a2a.utils.agent_to_a2a import to_a2a

    port = int(os.environ.get("ACCOUNT_AGENT_PORT", "8001"))
    agent = create_agent()
    to_a2a(agent=agent, port=port)
