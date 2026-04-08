"""A2A Agent #3 — Inventory Management Agent (port 8003).

Connects to the Inventory FastMCP server (SSE on port 9003).
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
    mcp_port = int(os.getenv("INVENTORY_MCP_PORT", "9003"))
    agent_port = int(os.getenv("INVENTORY_AGENT_PORT", "8003"))

    logger.info(f"📦 Inventory Management Agent connecting to MCP on port {mcp_port}")

    tools, exit_stack = await McpToolset.from_server(
        connection_params=SseConnectionParams(url=f"http://localhost:{mcp_port}/sse")
    )

    agent = Agent(
        model="gemini-3-flash-preview",
        name="inventory_management_agent",
        description="Specialist for stock management: check levels, update quantities, handle reservations, and low-stock alerts.",
        instruction=(
            "You are the Inventory Management specialist. Use your tools to:\n"
            "- Check stock levels for any product SKU\n"
            "- Update stock quantities after shipments or sales\n"
            "- Identify low-stock items that need reordering\n"
            "- Reserve stock for pending orders\n"
            "- Release reserved stock for cancelled orders\n"
            "Always report quantities clearly with warehouse info."
        ),
        tools=tools,
    )

    logger.info(f"📦 Inventory Management Agent starting A2A on port {agent_port}")
    app = to_a2a(agent, port=agent_port)
    await app


if __name__ == "__main__":
    asyncio.run(main())
