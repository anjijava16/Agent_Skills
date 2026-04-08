"""A2A Agent #8 — Returns & Refunds Agent (port 8008).

Connects to the Returns FastMCP server (SSE on port 9008).
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
    mcp_port = int(os.getenv("RETURNS_MCP_PORT", "9008"))
    agent_port = int(os.getenv("RETURNS_AGENT_PORT", "8008"))

    logger.info(f"🔁 Returns Agent connecting to MCP on port {mcp_port}")

    tools, exit_stack = await McpToolset.from_server(
        connection_params=SseConnectionParams(url=f"http://localhost:{mcp_port}/sse")
    )

    agent = Agent(
        model="gemini-3-flash-preview",
        name="returns_refunds_agent",
        description="Specialist for returns: initiate returns, track status, approve/reject, and process refunds.",
        instruction=(
            "You are the Returns & Refunds specialist. Use your tools to:\n"
            "- Initiate return requests for customers\n"
            "- Check return status and progress\n"
            "- Approve qualifying returns and set refund amounts\n"
            "- Process refunds for approved returns\n"
            "- List return history for a customer\n"
            "Guide customers through the return process step by step."
        ),
        tools=tools,
    )

    logger.info(f"🔁 Returns Agent starting A2A on port {agent_port}")
    app = to_a2a(agent, port=agent_port)
    await app


if __name__ == "__main__":
    asyncio.run(main())
