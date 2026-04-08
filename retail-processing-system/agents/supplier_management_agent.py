"""A2A Agent #10 — Supplier Management Agent (port 8010).

Connects to the Supplier FastMCP server (SSE on port 9010).
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
    mcp_port = int(os.getenv("SUPPLIER_MCP_PORT", "9010"))
    agent_port = int(os.getenv("SUPPLIER_AGENT_PORT", "8010"))

    logger.info(f"🏭 Supplier Management Agent connecting to MCP on port {mcp_port}")

    tools, exit_stack = await McpToolset.from_server(
        connection_params=SseConnectionParams(url=f"http://localhost:{mcp_port}/sse")
    )

    agent = Agent(
        model="gemini-3-flash-preview",
        name="supplier_management_agent",
        description="Specialist for suppliers: profiles, purchase orders, supply-chain status, and supplier ratings.",
        instruction=(
            "You are the Supplier Management specialist. Use your tools to:\n"
            "- Look up supplier profiles and contacts\n"
            "- Create purchase orders for restocking\n"
            "- Track purchase order status and delivery\n"
            "- List and filter suppliers by category or rating\n"
            "- Update supplier information and ratings\n"
            "Recommend reliable suppliers based on ratings and lead times."
        ),
        tools=tools,
    )

    logger.info(f"🏭 Supplier Management Agent starting A2A on port {agent_port}")
    app = to_a2a(agent, port=agent_port)
    await app


if __name__ == "__main__":
    asyncio.run(main())
