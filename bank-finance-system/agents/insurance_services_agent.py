"""Agent #8 — Insurance Services Agent (A2A on port 8008).

Connects to the Insurance Engine MCP server.
"""

import os

from google.adk.agents import Agent
from google.adk.tools.mcp import McpToolset, StdioConnectionParams

_MCP_SERVER = os.path.join(
    os.path.dirname(__file__), "..", "mcp_servers", "insurance_engine_server.py"
)


def create_agent() -> Agent:
    insurance_tools = McpToolset(
        connection_params=StdioConnectionParams(
            command="python",
            args=[_MCP_SERVER],
        )
    )
    return Agent(
        model="gemini-3-flash-preview",
        name="insurance_services_agent",
        description="Manages insurance — policy quotes, creation, claims filing, and claim tracking.",
        instruction=(
            "You are the Insurance Services specialist. "
            "Provide policy quotes, create new policies, file claims, "
            "track claim status, and list customer policies. "
            "Explain coverage details and premium breakdowns clearly."
        ),
        tools=[insurance_tools],
    )


if __name__ == "__main__":
    from google.adk.a2a.utils.agent_to_a2a import to_a2a

    port = int(os.environ.get("INSURANCE_AGENT_PORT", "8008"))
    agent = create_agent()
    to_a2a(agent=agent, port=port)
