"""Agent #7 — Investment & Portfolio Agent (A2A on port 8007).

Connects to the Market Data MCP server.
"""

import os

from google.adk.agents import Agent
from google.adk.tools.mcp import McpToolset, StdioConnectionParams

_MCP_SERVER = os.path.join(
    os.path.dirname(__file__), "..", "mcp_servers", "market_data_server.py"
)


def create_agent() -> Agent:
    market_tools = McpToolset(
        connection_params=StdioConnectionParams(
            command="python",
            args=[_MCP_SERVER],
        )
    )
    return Agent(
        model="gemini-3-flash-preview",
        name="investment_portfolio_agent",
        description="Manages investments — stock prices, portfolio tracking, buy/sell orders, and market summaries.",
        instruction=(
            "You are the Investment & Portfolio specialist. "
            "Provide stock prices, manage portfolio holdings, execute buy/sell orders, "
            "and generate market summaries. Always warn about investment risks. "
            "Present portfolio positions with current market values."
        ),
        tools=[market_tools],
    )


if __name__ == "__main__":
    from google.adk.a2a.utils.agent_to_a2a import to_a2a

    port = int(os.environ.get("INVESTMENT_AGENT_PORT", "8007"))
    agent = create_agent()
    to_a2a(agent=agent, port=port)
