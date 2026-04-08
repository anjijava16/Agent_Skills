"""A2A Agent #2 — Order Processing Agent (port 8002).

Connects to the Order Engine FastMCP server (SSE on port 9002).
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
    mcp_port = int(os.getenv("ORDER_MCP_PORT", "9002"))
    agent_port = int(os.getenv("ORDER_AGENT_PORT", "8002"))

    logger.info(f"📦 Order Processing Agent connecting to MCP on port {mcp_port}")

    tools, exit_stack = await McpToolset.from_server(
        connection_params=SseConnectionParams(url=f"http://localhost:{mcp_port}/sse")
    )

    agent = Agent(
        model="gemini-3-flash-preview",
        name="order_processing_agent",
        description="Specialist for order lifecycle: creation, status updates, cancellation, and history lookups.",
        instruction=(
            "You are the Order Processing specialist. Use your tools to:\n"
            "- Create new orders with items and customer info\n"
            "- Check order status and details\n"
            "- Update order status through the fulfillment pipeline\n"
            "- Cancel orders when requested\n"
            "- Retrieve order history for a customer\n"
            "Provide clear order confirmations with IDs."
        ),
        tools=tools,
    )

    logger.info(f"📦 Order Processing Agent starting A2A on port {agent_port}")
    app = to_a2a(agent, port=agent_port)
    await app


if __name__ == "__main__":
    asyncio.run(main())
