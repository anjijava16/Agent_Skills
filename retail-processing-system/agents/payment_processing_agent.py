"""A2A Agent #5 — Payment Processing Agent (port 8005).

Connects to the Payment Gateway FastMCP server (SSE on port 9005).
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
    mcp_port = int(os.getenv("PAYMENT_MCP_PORT", "9005"))
    agent_port = int(os.getenv("PAYMENT_AGENT_PORT", "8005"))

    logger.info(f"💳 Payment Processing Agent connecting to MCP on port {mcp_port}")

    tools, exit_stack = await McpToolset.from_server(
        connection_params=SseConnectionParams(url=f"http://localhost:{mcp_port}/sse")
    )

    agent = Agent(
        model="gemini-3-flash-preview",
        name="payment_processing_agent",
        description="Specialist for payments: process charges, refunds, transaction lookup, and payment verification.",
        instruction=(
            "You are the Payment Processing specialist. Use your tools to:\n"
            "- Process payments for orders\n"
            "- Issue full or partial refunds\n"
            "- Check payment/transaction status\n"
            "- List transactions for a customer or order\n"
            "- Verify payment authenticity\n"
            "Never expose full card numbers. Report amounts clearly."
        ),
        tools=tools,
    )

    logger.info(f"💳 Payment Processing Agent starting A2A on port {agent_port}")
    app = to_a2a(agent, port=agent_port)
    await app


if __name__ == "__main__":
    asyncio.run(main())
