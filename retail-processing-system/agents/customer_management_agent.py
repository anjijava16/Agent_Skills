"""A2A Agent #4 — Customer Management Agent (port 8004).

Connects to the Customer DB FastMCP server (SSE on port 9004).
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
    mcp_port = int(os.getenv("CUSTOMER_MCP_PORT", "9004"))
    agent_port = int(os.getenv("CUSTOMER_AGENT_PORT", "8004"))

    logger.info(f"👤 Customer Management Agent connecting to MCP on port {mcp_port}")

    tools, exit_stack = await McpToolset.from_server(
        connection_params=SseConnectionParams(url=f"http://localhost:{mcp_port}/sse")
    )

    agent = Agent(
        model="gemini-3-flash-preview",
        name="customer_management_agent",
        description="Specialist for customer profiles: registration, updates, loyalty points, and customer search.",
        instruction=(
            "You are the Customer Management specialist. Use your tools to:\n"
            "- Look up customer profiles by ID\n"
            "- Register new customers\n"
            "- Update customer information and tier\n"
            "- Check loyalty points balance and tier benefits\n"
            "- Search customers by name or email\n"
            "Handle customer data with care and respect privacy."
        ),
        tools=tools,
    )

    logger.info(f"👤 Customer Management Agent starting A2A on port {agent_port}")
    app = to_a2a(agent, port=agent_port)
    await app


if __name__ == "__main__":
    asyncio.run(main())
