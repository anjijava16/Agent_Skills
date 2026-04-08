"""Agent #3 — Loan Management Agent (A2A on port 8003).

Connects to the Loan Engine MCP server.
"""

import os

from google.adk.agents import Agent
from google.adk.tools.mcp import McpToolset, StdioConnectionParams

_MCP_SERVER = os.path.join(
    os.path.dirname(__file__), "..", "mcp_servers", "loan_engine_server.py"
)


def create_agent() -> Agent:
    loan_tools = McpToolset(
        connection_params=StdioConnectionParams(
            command="python",
            args=[_MCP_SERVER],
        )
    )
    return Agent(
        model="gemini-3-flash-preview",
        name="loan_management_agent",
        description="Manages loans — applications, EMI calculations, approval, and repayment schedules.",
        instruction=(
            "You are the Loan Management specialist. "
            "Help customers apply for loans, calculate EMI, check loan status, "
            "and review repayment schedules. Verify eligibility before approvals. "
            "Present clear breakdowns of interest rates and payment plans."
        ),
        tools=[loan_tools],
    )


if __name__ == "__main__":
    from google.adk.a2a.utils.agent_to_a2a import to_a2a

    port = int(os.environ.get("LOAN_AGENT_PORT", "8003"))
    agent = create_agent()
    to_a2a(agent=agent, port=port)
