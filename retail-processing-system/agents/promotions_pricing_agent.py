"""A2A Agent #7 — Promotions & Pricing Agent (port 8007).

Connects to the Promotions FastMCP server (SSE on port 9007).
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
    mcp_port = int(os.getenv("PROMOTIONS_MCP_PORT", "9007"))
    agent_port = int(os.getenv("PROMOTIONS_AGENT_PORT", "8007"))

    logger.info(f"🏷️ Promotions Agent connecting to MCP on port {mcp_port}")

    tools, exit_stack = await McpToolset.from_server(
        connection_params=SseConnectionParams(url=f"http://localhost:{mcp_port}/sse")
    )

    agent = Agent(
        model="gemini-3-flash-preview",
        name="promotions_pricing_agent",
        description="Specialist for promotions and pricing: apply coupons, calculate discounts, manage active promotions.",
        instruction=(
            "You are the Promotions & Pricing specialist. Use your tools to:\n"
            "- Apply coupon codes to orders and calculate savings\n"
            "- Show all active promotions\n"
            "- Preview discount amounts before applying\n"
            "- Create new promotional campaigns\n"
            "- Validate coupon codes for usability\n"
            "Always show original price, discount, and final price."
        ),
        tools=tools,
    )

    logger.info(f"🏷️ Promotions Agent starting A2A on port {agent_port}")
    app = to_a2a(agent, port=agent_port)
    await app


if __name__ == "__main__":
    asyncio.run(main())
