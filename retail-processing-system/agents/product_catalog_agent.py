"""A2A Agent #1 — Product Catalog Agent (port 8001).

Connects to the Product Catalog FastMCP server (SSE on port 9001) and exposes
an A2A endpoint for the orchestrator.
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
    mcp_port = int(os.getenv("PRODUCT_MCP_PORT", "9001"))
    agent_port = int(os.getenv("PRODUCT_AGENT_PORT", "8001"))

    logger.info(f"🛍️ Product Catalog Agent connecting to MCP on port {mcp_port}")

    tools, exit_stack = await McpToolset.from_server(
        connection_params=SseConnectionParams(url=f"http://localhost:{mcp_port}/sse")
    )

    agent = Agent(
        model="gemini-3-flash-preview",
        name="product_catalog_agent",
        description="Specialist for product catalog operations: search, browse, create, and update products and categories.",
        instruction=(
            "You are the Product Catalog specialist. Use your tools to:\n"
            "- Look up products by SKU or search by keyword\n"
            "- List available product categories\n"
            "- Create new products with full details\n"
            "- Update existing product information\n"
            "Always return structured, clear responses."
        ),
        tools=tools,
    )

    logger.info(f"🛍️ Product Catalog Agent starting A2A on port {agent_port}")
    app = to_a2a(agent, port=agent_port)
    await app


if __name__ == "__main__":
    asyncio.run(main())
