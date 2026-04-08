"""FastMCP Server #3 — Inventory Management (port 9003).

Tools for stock levels, alerts, reservations, and restocking.
"""

import asyncio
import logging
import os
from typing import Optional

from fastmcp import FastMCP

logger = logging.getLogger(__name__)
logging.basicConfig(format="[%(levelname)s]: %(message)s", level=logging.INFO)

mcp = FastMCP("Inventory Management MCP Server 📊")

# ---------------------------------------------------------------------------
# In-memory inventory store
# ---------------------------------------------------------------------------

INVENTORY = {
    "SKU-1001": {"sku": "SKU-1001", "name": "Wireless Bluetooth Headphones", "quantity": 150, "reserved": 5, "reorder_level": 20, "warehouse": "WH-EAST"},
    "SKU-1002": {"sku": "SKU-1002", "name": "Organic Cotton T-Shirt", "quantity": 500, "reserved": 12, "reorder_level": 50, "warehouse": "WH-WEST"},
    "SKU-1003": {"sku": "SKU-1003", "name": "Stainless Steel Water Bottle", "quantity": 8, "reserved": 0, "reorder_level": 25, "warehouse": "WH-EAST"},
    "SKU-1004": {"sku": "SKU-1004", "name": "Smart LED Desk Lamp", "quantity": 75, "reserved": 3, "reorder_level": 15, "warehouse": "WH-CENTRAL"},
    "SKU-1005": {"sku": "SKU-1005", "name": "Trail Mix Variety Pack", "quantity": 3, "reserved": 0, "reorder_level": 100, "warehouse": "WH-WEST"},
}


@mcp.tool()
def check_stock(sku: str) -> dict:
    """Check current stock level for a product.

    Args:
        sku: Product SKU to check (e.g., 'SKU-1001').

    Returns:
        Stock details including available quantity (total minus reserved).
    """
    logger.info(f"--- 📊 check_stock {sku} ---")
    item = INVENTORY.get(sku)
    if not item:
        return {"error": f"SKU {sku} not found in inventory"}
    available = item["quantity"] - item["reserved"]
    return {**item, "available": available}


@mcp.tool()
def update_stock(sku: str, quantity_change: int, reason: str = "") -> dict:
    """Add or remove stock for a product.

    Args:
        sku: Product SKU to update.
        quantity_change: Positive to add stock, negative to remove.
        reason: Reason for the adjustment (e.g., 'restock', 'damaged').

    Returns:
        Updated stock level.
    """
    logger.info(f"--- ✏️ update_stock {sku} by {quantity_change} ---")
    item = INVENTORY.get(sku)
    if not item:
        return {"error": f"SKU {sku} not found in inventory"}
    new_qty = item["quantity"] + quantity_change
    if new_qty < 0:
        return {"error": f"Cannot reduce below 0. Current: {item['quantity']}, change: {quantity_change}"}
    item["quantity"] = new_qty
    available = new_qty - item["reserved"]
    return {"status": "updated", "sku": sku, "quantity": new_qty, "available": available, "reason": reason}


@mcp.tool()
def get_low_stock_alerts(threshold_multiplier: float = 1.0) -> dict:
    """Get products that are at or below their reorder level.

    Args:
        threshold_multiplier: Multiplier for reorder level. Use 1.0 for exact reorder level,
                               1.5 to catch items approaching reorder level.

    Returns:
        List of low-stock products needing reorder.
    """
    logger.info(f"--- ⚠️ get_low_stock_alerts (multiplier={threshold_multiplier}) ---")
    alerts = []
    for item in INVENTORY.values():
        threshold = item["reorder_level"] * threshold_multiplier
        available = item["quantity"] - item["reserved"]
        if available <= threshold:
            alerts.append({
                "sku": item["sku"],
                "name": item["name"],
                "available": available,
                "reorder_level": item["reorder_level"],
                "warehouse": item["warehouse"],
                "severity": "critical" if available <= 0 else "warning",
            })
    alerts.sort(key=lambda x: x["available"])
    return {"alerts": alerts, "count": len(alerts)}


@mcp.tool()
def reserve_stock(sku: str, quantity: int, order_id: str = "") -> dict:
    """Reserve stock for an order (reduces available but not total quantity).

    Args:
        sku: Product SKU to reserve.
        quantity: Number of units to reserve.
        order_id: Associated order ID for tracking.

    Returns:
        Reservation status and remaining availability.
    """
    logger.info(f"--- 🔒 reserve_stock {sku} x{quantity} ---")
    item = INVENTORY.get(sku)
    if not item:
        return {"error": f"SKU {sku} not found in inventory"}
    available = item["quantity"] - item["reserved"]
    if quantity > available:
        return {"error": f"Insufficient stock. Available: {available}, requested: {quantity}"}
    item["reserved"] += quantity
    return {
        "status": "reserved",
        "sku": sku,
        "reserved_qty": quantity,
        "order_id": order_id,
        "remaining_available": item["quantity"] - item["reserved"],
    }


@mcp.tool()
def release_stock(sku: str, quantity: int, reason: str = "") -> dict:
    """Release previously reserved stock (e.g., order cancelled).

    Args:
        sku: Product SKU to release.
        quantity: Number of units to release from reservation.
        reason: Reason for release (e.g., 'order_cancelled').

    Returns:
        Updated reservation status.
    """
    logger.info(f"--- 🔓 release_stock {sku} x{quantity} ---")
    item = INVENTORY.get(sku)
    if not item:
        return {"error": f"SKU {sku} not found in inventory"}
    if quantity > item["reserved"]:
        return {"error": f"Cannot release {quantity}, only {item['reserved']} reserved"}
    item["reserved"] -= quantity
    return {
        "status": "released",
        "sku": sku,
        "released_qty": quantity,
        "remaining_reserved": item["reserved"],
        "available": item["quantity"] - item["reserved"],
        "reason": reason,
    }


if __name__ == "__main__":
    port = int(os.getenv("INVENTORY_MCP_PORT", "9003"))
    logger.info(f"📊 Inventory MCP starting on port {port}")
    asyncio.run(mcp.run_async(transport="sse", host="0.0.0.0", port=port))
