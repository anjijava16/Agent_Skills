"""Agent #10 — Audit & Compliance Agent (A2A on port 8010).

Connects to the Audit Ledger MCP server.
"""

import os

from google.adk.agents import Agent
from google.adk.tools.mcp import McpToolset, StdioConnectionParams

_MCP_SERVER = os.path.join(
    os.path.dirname(__file__), "..", "mcp_servers", "audit_ledger_server.py"
)


def create_agent() -> Agent:
    audit_tools = McpToolset(
        connection_params=StdioConnectionParams(
            command="python",
            args=[_MCP_SERVER],
        )
    )
    return Agent(
        model="gemini-3-flash-preview",
        name="audit_compliance_agent",
        description="Manages audit trails, compliance checks, regulatory reports, and banking regulations.",
        instruction=(
            "You are the Audit & Compliance specialist. "
            "Log audit events, retrieve audit trails, generate compliance reports, "
            "check action compliance against regulations, and list applicable regulations. "
            "Maintain strict accuracy — audit records must be immutable and complete."
        ),
        tools=[audit_tools],
    )


if __name__ == "__main__":
    from google.adk.a2a.utils.agent_to_a2a import to_a2a

    port = int(os.environ.get("AUDIT_AGENT_PORT", "8010"))
    agent = create_agent()
    to_a2a(agent=agent, port=port)
