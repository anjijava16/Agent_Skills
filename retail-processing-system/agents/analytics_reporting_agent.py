"""A2A Agent #9 — Analytics & Reporting Agent (port 8009).

Connects to the Analytics FastMCP server (SSE on port 9009).
"""

import asyncio
import logging
import os

from google.adk.agents import Agent
from google.adk.tools.mcp import McpToolset, SseConnectionParams
from google.adk.endpoints import to_a2a

logger = logging.getLogger(__name__)
logging.basicConfig(format="[%(levelname)s]: %(message)s", level=logging.INFO)


async def main():
    mcp_port = int(os.getenv("ANALYTICS_MCP_PORT", "9009"))
    agent_port = int(os.getenv("ANALYTICS_AGENT_PORT", "8009"))

    logger.info(f"📊 Analytics Agent connecting to MCP on port {mcp_port}")

    tools, exit_stack = await McpToolset.from_server(
        connection_params=SseConnectionParams(url=f"http://localhost:{mcp_port}/sse")
    )

    agent = Agent(
        model="gemini-3-flash-preview",
        name="analytics_reporting_agent",
        description="Specialist for analytics: sales summaries, top products, revenue reports, customer metrics, and inventory turnover.",
        instruction=(
            "You are the Analytics & Reporting specialist. Use your tools to:\n"
            "- Get monthly sales summaries and trends\n"
            "- Identify top-selling products by revenue or units\n"
            "- Generate revenue reports across time periods\n"
            "- Provide customer metrics and churn analysis\n"
            "- Report inventory turnover rates\n"
            "Present data clearly with numbers and comparisons."
        ),
        tools=tools,
    )

    logger.info(f"📊 Analytics Agent starting A2A on port {agent_port}")
    app = to_a2a(agent, port=agent_port)
    await app


if __name__ == "__main__":
    asyncio.run(main())
