"""Retail Processing Orchestrator Agent (port 8000).

Routes user requests to the appropriate specialist agent via A2A protocol.
All 10 specialist agents must be running before starting this orchestrator.
"""

import asyncio
import logging
import os

from google.adk.agents import Agent
from google.adk.agents.remote_a2a_agent import RemoteA2aAgent
from google.adk.endpoints import to_a2a

logger = logging.getLogger(__name__)
logging.basicConfig(format="[%(levelname)s]: %(message)s", level=logging.INFO)


def _agent_url(port: int) -> str:
    host = os.getenv("AGENT_HOST", "localhost")
    return f"http://{host}:{port}/.well-known/agent.json"


async def main():
    orch_port = int(os.getenv("ORCHESTRATOR_PORT", "8000"))

    # -------------------------------------------------------------------
    # Connect to all 10 specialist A2A agents
    # -------------------------------------------------------------------
    specialists = {
        "product_catalog": int(os.getenv("PRODUCT_AGENT_PORT", "8001")),
        "order_processing": int(os.getenv("ORDER_AGENT_PORT", "8002")),
        "inventory_management": int(os.getenv("INVENTORY_AGENT_PORT", "8003")),
        "customer_management": int(os.getenv("CUSTOMER_AGENT_PORT", "8004")),
        "payment_processing": int(os.getenv("PAYMENT_AGENT_PORT", "8005")),
        "shipping_logistics": int(os.getenv("SHIPPING_AGENT_PORT", "8006")),
        "promotions_pricing": int(os.getenv("PROMOTIONS_AGENT_PORT", "8007")),
        "returns_refunds": int(os.getenv("RETURNS_AGENT_PORT", "8008")),
        "analytics_reporting": int(os.getenv("ANALYTICS_AGENT_PORT", "8009")),
        "supplier_management": int(os.getenv("SUPPLIER_AGENT_PORT", "8010")),
    }

    remote_agents = []
    for name, port in specialists.items():
        url = _agent_url(port)
        logger.info(f"🔗 Connecting to {name} at {url}")
        remote_agents.append(
            RemoteA2aAgent(agent_card=url)
        )

    # -------------------------------------------------------------------
    # Orchestrator agent with sub-agents
    # -------------------------------------------------------------------
    orchestrator = Agent(
        model="gemini-3-flash-preview",
        name="retail_orchestrator",
        description="Central orchestrator for the Retail Processing multi-agent system.",
        instruction=(
            "You are the Retail Processing Orchestrator. You coordinate a team of "
            "10 specialist agents to handle any retail operation.\n\n"
            "ROUTING GUIDE — delegate to the right specialist:\n"
            "• Product searches, catalog browsing, product creation → product_catalog_agent\n"
            "• Order creation, status, cancellation, history → order_processing_agent\n"
            "• Stock checks, inventory updates, low-stock alerts → inventory_management_agent\n"
            "• Customer profiles, registration, loyalty points → customer_management_agent\n"
            "• Payments, refunds, transaction lookups → payment_processing_agent\n"
            "• Shipping, tracking, rate quotes, carriers → shipping_logistics_agent\n"
            "• Coupons, discounts, promotions → promotions_pricing_agent\n"
            "• Return requests, return status, refund processing → returns_refunds_agent\n"
            "• Sales reports, analytics, metrics, dashboards → analytics_reporting_agent\n"
            "• Supplier info, purchase orders, supply chain → supplier_management_agent\n\n"
            "For complex requests that span multiple domains (e.g., 'place an order, apply a coupon, "
            "and arrange shipping'), coordinate across multiple specialists sequentially.\n"
            "Always provide a clear, consolidated response to the user."
        ),
        sub_agents=remote_agents,
    )

    logger.info(f"🚀 Retail Orchestrator starting A2A on port {orch_port}")
    app = to_a2a(orchestrator, port=orch_port)
    await app


if __name__ == "__main__":
    asyncio.run(main())
