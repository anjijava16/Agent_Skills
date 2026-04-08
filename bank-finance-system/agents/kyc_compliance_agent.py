"""Agent #6 — KYC & Compliance Agent (A2A on port 8006).

Connects to the KYC Registry MCP server.
"""

import os

from google.adk.agents import Agent
from google.adk.tools.mcp import McpToolset, StdioConnectionParams

_MCP_SERVER = os.path.join(
    os.path.dirname(__file__), "..", "mcp_servers", "kyc_registry_server.py"
)


def create_agent() -> Agent:
    kyc_tools = McpToolset(
        connection_params=StdioConnectionParams(
            command="python",
            args=[_MCP_SERVER],
        )
    )
    return Agent(
        model="gemini-3-flash-preview",
        name="kyc_compliance_agent",
        description="Handles KYC verification, document checks, AML screening, and compliance status.",
        instruction=(
            "You are the KYC & Compliance specialist. "
            "Verify customer identities, check document validity, run AML screenings, "
            "and report KYC status. Enforce regulatory requirements strictly. "
            "Never approve incomplete or suspicious KYC submissions."
        ),
        tools=[kyc_tools],
    )


if __name__ == "__main__":
    from google.adk.a2a.utils.agent_to_a2a import to_a2a

    port = int(os.environ.get("KYC_AGENT_PORT", "8006"))
    agent = create_agent()
    to_a2a(agent=agent, port=port)
