"""Agent #2 — Transaction Processing Agent (A2A on port 8002).

Connects to the Transaction Engine MCP server.
"""

import os

from google.adk.agents import Agent
from google.adk.tools.mcp import McpToolset, StdioConnectionParams

_MCP_SERVER = os.path.join(
    os.path.dirname(__file__), "..", "mcp_servers", "transaction_engine_server.py"
)


def create_agent() -> Agent:
    txn_tools = McpToolset(
        connection_params=StdioConnectionParams(
            command="python",
            args=[_MCP_SERVER],
        )
    )
    return Agent(
        model="gemini-3-flash-preview",
        name="transaction_processing_agent",
        description="Processes financial transactions — transfers, payments, history, and statements.",
        instruction=(
            "You are the Transaction Processing specialist. "
            "Handle fund transfers, bill payments, and statement generation. "
            "Always verify account IDs and amounts before processing. "
            "Report transaction status clearly."
        ),
        tools=[txn_tools],
    )


if __name__ == "__main__":
    from google.adk.a2a.utils.agent_to_a2a import to_a2a

    port = int(os.environ.get("TRANSACTION_AGENT_PORT", "8002"))
    agent = create_agent()
    to_a2a(agent=agent, port=port)
