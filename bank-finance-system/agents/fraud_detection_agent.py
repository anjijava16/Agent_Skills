"""Agent #5 — Fraud Detection Agent (A2A on port 8005).

Connects to the Fraud Engine MCP server.
"""

import os

from google.adk.agents import Agent
from google.adk.tools.mcp import McpToolset, StdioConnectionParams

_MCP_SERVER = os.path.join(
    os.path.dirname(__file__), "..", "mcp_servers", "fraud_engine_server.py"
)


def create_agent() -> Agent:
    fraud_tools = McpToolset(
        connection_params=StdioConnectionParams(
            command="python",
            args=[_MCP_SERVER],
        )
    )
    return Agent(
        model="gemini-3-flash-preview",
        name="fraud_detection_agent",
        description="Detects and manages fraud — risk scoring, suspicious flagging, alerts, and verification.",
        instruction=(
            "You are the Fraud Detection specialist. "
            "Analyze transactions for risk, flag suspicious activity, review fraud alerts, "
            "and verify or reject flagged transactions. "
            "Err on the side of caution — flag when uncertain. "
            "Provide clear risk scores and justifications."
        ),
        tools=[fraud_tools],
    )


if __name__ == "__main__":
    from google.adk.a2a.utils.agent_to_a2a import to_a2a

    port = int(os.environ.get("FRAUD_AGENT_PORT", "8005"))
    agent = create_agent()
    to_a2a(agent=agent, port=port)
