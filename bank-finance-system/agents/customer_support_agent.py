"""Agent #9 — Customer Support Agent (A2A on port 8009).

Connects to the Support Ticketing MCP server.
"""

import os

from google.adk.agents import Agent
from google.adk.tools.mcp import McpToolset, StdioConnectionParams

_MCP_SERVER = os.path.join(
    os.path.dirname(__file__), "..", "mcp_servers", "support_ticketing_server.py"
)


def create_agent() -> Agent:
    support_tools = McpToolset(
        connection_params=StdioConnectionParams(
            command="python",
            args=[_MCP_SERVER],
        )
    )
    return Agent(
        model="gemini-3-flash-preview",
        name="customer_support_agent",
        description="Handles customer support — ticket creation, status tracking, FAQ search, and escalation.",
        instruction=(
            "You are the Customer Support specialist. "
            "Create support tickets, check ticket status, update tickets, "
            "search FAQs for quick answers, and escalate urgent issues. "
            "Be empathetic and solution-oriented. Try FAQ first before creating tickets."
        ),
        tools=[support_tools],
    )


if __name__ == "__main__":
    from google.adk.a2a.utils.agent_to_a2a import to_a2a

    port = int(os.environ.get("SUPPORT_AGENT_PORT", "8009"))
    agent = create_agent()
    to_a2a(agent=agent, port=port)
