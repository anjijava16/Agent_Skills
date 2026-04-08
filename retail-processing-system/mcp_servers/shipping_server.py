"""FastMCP Server #6 — Shipping & Logistics (port 9006).

Tools for shipment creation, tracking, rate quotes, and carrier management.
"""

import asyncio
import logging
import os
import uuid
from datetime import datetime, timedelta
from typing import Optional

from fastmcp import FastMCP

logger = logging.getLogger(__name__)
logging.basicConfig(format="[%(levelname)s]: %(message)s", level=logging.INFO)

mcp = FastMCP("Shipping & Logistics MCP Server 🚚")

# ---------------------------------------------------------------------------
# In-memory shipment & carrier stores
# ---------------------------------------------------------------------------

CARRIERS = {
    "CARRIER-FE": {"carrier_id": "CARRIER-FE", "name": "FedEx", "services": ["standard", "express", "overnight"]},
    "CARRIER-UP": {"carrier_id": "CARRIER-UP", "name": "UPS", "services": ["ground", "2day", "next_day"]},
    "CARRIER-US": {"carrier_id": "CARRIER-US", "name": "USPS", "services": ["priority", "first_class", "media"]},
}

SHIPMENTS = {
    "SHP-6001": {
        "shipment_id": "SHP-6001",
        "order_id": "ORD-2001",
        "carrier_id": "CARRIER-FE",
        "service": "standard",
        "tracking_number": "FE123456789",
        "status": "delivered",
        "origin": "Warehouse A, TX",
        "destination": "123 Main St, NY 10001",
        "shipped_at": "2025-01-11T08:00:00Z",
        "delivered_at": "2025-01-14T15:30:00Z",
    },
    "SHP-6002": {
        "shipment_id": "SHP-6002",
        "order_id": "ORD-2002",
        "carrier_id": "CARRIER-UP",
        "service": "ground",
        "tracking_number": "UP987654321",
        "status": "in_transit",
        "origin": "Warehouse B, CA",
        "destination": "456 Oak Ave, IL 60601",
        "shipped_at": "2025-01-13T10:00:00Z",
        "delivered_at": None,
    },
}


@mcp.tool()
def create_shipment(
    order_id: str,
    carrier_id: str,
    service: str,
    destination: str,
    origin: str = "Warehouse A, TX",
) -> dict:
    """Create a new shipment for an order.

    Args:
        order_id: The order to ship.
        carrier_id: Carrier identifier (e.g., 'CARRIER-FE').
        service: Shipping service level (e.g., 'standard', 'express').
        destination: Delivery address.
        origin: Origin warehouse.

    Returns:
        Shipment confirmation with tracking number.
    """
    logger.info(f"--- 📦 create_shipment ORD={order_id} ---")
    carrier = CARRIERS.get(carrier_id)
    if not carrier:
        return {"error": f"Carrier {carrier_id} not found"}
    if service not in carrier["services"]:
        return {"error": f"Service '{service}' not available for {carrier['name']}"}
    shp_id = f"SHP-{uuid.uuid4().hex[:4].upper()}"
    tracking = f"{carrier['name'][:2].upper()}{uuid.uuid4().hex[:9].upper()}"
    shipment = {
        "shipment_id": shp_id,
        "order_id": order_id,
        "carrier_id": carrier_id,
        "service": service,
        "tracking_number": tracking,
        "status": "label_created",
        "origin": origin,
        "destination": destination,
        "shipped_at": None,
        "delivered_at": None,
    }
    SHIPMENTS[shp_id] = shipment
    return {"status": "shipment_created", "shipment": shipment}


@mcp.tool()
def track_shipment(shipment_id: str) -> dict:
    """Get current tracking info for a shipment.

    Args:
        shipment_id: Shipment to track.

    Returns:
        Current tracking status and timeline.
    """
    logger.info(f"--- 📍 track_shipment {shipment_id} ---")
    shipment = SHIPMENTS.get(shipment_id)
    if not shipment:
        return {"error": f"Shipment {shipment_id} not found"}
    return {
        "shipment_id": shipment["shipment_id"],
        "tracking_number": shipment["tracking_number"],
        "carrier": CARRIERS.get(shipment["carrier_id"], {}).get("name", "Unknown"),
        "status": shipment["status"],
        "origin": shipment["origin"],
        "destination": shipment["destination"],
        "shipped_at": shipment["shipped_at"],
        "delivered_at": shipment["delivered_at"],
    }


@mcp.tool()
def get_shipping_rates(
    destination: str,
    weight_lbs: float = 2.0,
    origin: str = "Warehouse A, TX",
) -> dict:
    """Get rate quotes from all carriers.

    Args:
        destination: Delivery address or zip code.
        weight_lbs: Package weight in pounds.
        origin: Origin warehouse.

    Returns:
        Rate quotes per carrier and service level.
    """
    logger.info(f"--- 💲 get_shipping_rates to {destination} ---")
    base_rate = 5.99 + (weight_lbs * 0.80)
    quotes = []
    multipliers = {"standard": 1.0, "express": 1.8, "overnight": 3.0,
                   "ground": 0.9, "2day": 1.6, "next_day": 2.8,
                   "priority": 1.2, "first_class": 0.7, "media": 0.5}
    for carrier in CARRIERS.values():
        for svc in carrier["services"]:
            mult = multipliers.get(svc, 1.0)
            quotes.append({
                "carrier": carrier["name"],
                "carrier_id": carrier["carrier_id"],
                "service": svc,
                "rate_usd": round(base_rate * mult, 2),
                "estimated_days": max(1, int(5 / mult)),
            })
    quotes.sort(key=lambda q: q["rate_usd"])
    return {"origin": origin, "destination": destination, "weight_lbs": weight_lbs, "quotes": quotes}


@mcp.tool()
def update_delivery(
    shipment_id: str,
    status: str,
) -> dict:
    """Update the delivery status of a shipment.

    Args:
        shipment_id: Shipment to update.
        status: New status — 'label_created', 'picked_up', 'in_transit', 'out_for_delivery', 'delivered', 'exception'.

    Returns:
        Updated shipment details.
    """
    logger.info(f"--- 🔄 update_delivery {shipment_id} → {status} ---")
    valid = {"label_created", "picked_up", "in_transit", "out_for_delivery", "delivered", "exception"}
    if status not in valid:
        return {"error": f"Invalid status: {status}. Must be one of {valid}"}
    shipment = SHIPMENTS.get(shipment_id)
    if not shipment:
        return {"error": f"Shipment {shipment_id} not found"}
    shipment["status"] = status
    now = datetime.utcnow().isoformat() + "Z"
    if status == "picked_up" and not shipment["shipped_at"]:
        shipment["shipped_at"] = now
    if status == "delivered":
        shipment["delivered_at"] = now
    return {"status": "updated", "shipment": shipment}


@mcp.tool()
def list_carriers() -> dict:
    """List all available shipping carriers and their services.

    Returns:
        All carriers with service levels.
    """
    logger.info("--- 🏢 list_carriers ---")
    return {"carriers": list(CARRIERS.values()), "count": len(CARRIERS)}


if __name__ == "__main__":
    port = int(os.getenv("SHIPPING_MCP_PORT", "9006"))
    logger.info(f"🚚 Shipping MCP starting on port {port}")
    asyncio.run(mcp.run_async(transport="sse", host="0.0.0.0", port=port))
