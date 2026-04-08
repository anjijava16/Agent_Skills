"""A2A Agent #6 — Shipping & Logistics Agent (port 8006).

Connects to the Shipping FastMCP server (SSE on port 9006).
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
    mcp_port = int(os.getenv("SHIPPING_MCP_PORT", "9006"))
    agent_port = int(os.getenv("SHIPPING_AGENT_PORT", "8006"))

    logger.info(f"🚚 Shipping Agent connecting to MCP on port {mcp_port}")

    tools, exit_stack = await McpToolset.from_server(
        connection_params=SseConnectionParams(url=f"http://localhost:{mcp_port}/sse")
    )

    agent = Agent(
        model="gemini-3-flash-preview",
        name="shipping_logistics_agent",
        description="Specialist for shipping: create shipments, track packages, get rate quotes, and manage deliveries.",
        instruction=(
            "You are the Shipping & Logistics specialist. Use your tools to:\n"
            "- Create shipments and get tracking numbers\n"
            "- Track shipment status and delivery ETA\n"
            "- Get shipping rate quotes from all carriers\n"
            "- Update delivery status milestones\n"
            "- List available carriers and services\n"
            "Recommend the best shipping option based on speed and cost."
        ),
        tools=tools,
    )

    logger.info(f"🚚 Shipping Agent starting A2A on port {agent_port}")
    app = to_a2a(agent, port=agent_port)
    await app


if __name__ == "__main__":
    asyncio.run(main())
