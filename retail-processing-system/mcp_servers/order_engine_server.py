"""FastMCP Server #2 — Order Engine (port 9002).

Tools for order creation, tracking, status updates, and history.
"""

import asyncio
import logging
import os
import uuid
from datetime import datetime
from typing import Optional

from fastmcp import FastMCP

logger = logging.getLogger(__name__)
logging.basicConfig(format="[%(levelname)s]: %(message)s", level=logging.INFO)

mcp = FastMCP("Order Engine MCP Server 📦")

# ---------------------------------------------------------------------------
# In-memory order store
# ---------------------------------------------------------------------------

ORDERS = {
    "ORD-2001": {
        "order_id": "ORD-2001",
        "customer_id": "CUST-100",
        "items": [{"sku": "SKU-1001", "qty": 1, "unit_price": 79.99}],
        "total": 79.99,
        "status": "delivered",
        "created_at": "2024-05-10T14:30:00Z",
    },
    "ORD-2002": {
        "order_id": "ORD-2002",
        "customer_id": "CUST-101",
        "items": [
            {"sku": "SKU-1002", "qty": 2, "unit_price": 24.99},
            {"sku": "SKU-1003", "qty": 1, "unit_price": 18.50},
        ],
        "total": 68.48,
        "status": "processing",
        "created_at": "2024-06-15T09:00:00Z",
    },
}


@mcp.tool()
def create_order(customer_id: str, items: list[dict]) -> dict:
    """Create a new retail order.

    Args:
        customer_id: The customer placing the order (e.g., 'CUST-100').
        items: List of line items. Each dict must have 'sku', 'qty', 'unit_price'.
               Example: [{"sku": "SKU-1001", "qty": 2, "unit_price": 79.99}]

    Returns:
        The created order with ID, total, and status.
    """
    logger.info(f"--- ➕ create_order for customer {customer_id} ---")
    order_id = f"ORD-{uuid.uuid4().hex[:4].upper()}"
    total = sum(i["qty"] * i["unit_price"] for i in items)
    order = {
        "order_id": order_id,
        "customer_id": customer_id,
        "items": items,
        "total": round(total, 2),
        "status": "pending",
        "created_at": datetime.utcnow().isoformat() + "Z",
    }
    ORDERS[order_id] = order
    return {"status": "created", "order": order}


@mcp.tool()
def get_order(order_id: str) -> dict:
    """Get full details of an order.

    Args:
        order_id: The order identifier (e.g., 'ORD-2001').

    Returns:
        Order details or error if not found.
    """
    logger.info(f"--- 🔍 get_order {order_id} ---")
    order = ORDERS.get(order_id)
    if not order:
        return {"error": f"Order {order_id} not found"}
    return order


@mcp.tool()
def update_order_status(order_id: str, new_status: str) -> dict:
    """Update the status of an order.

    Args:
        order_id: The order to update.
        new_status: New status — one of 'pending', 'processing', 'shipped', 'delivered', 'cancelled'.

    Returns:
        Updated order details.
    """
    logger.info(f"--- ✏️ update_order_status {order_id} → {new_status} ---")
    valid = {"pending", "processing", "shipped", "delivered", "cancelled"}
    if new_status not in valid:
        return {"error": f"Invalid status. Must be one of: {', '.join(valid)}"}
    order = ORDERS.get(order_id)
    if not order:
        return {"error": f"Order {order_id} not found"}
    order["status"] = new_status
    return {"status": "updated", "order": order}


@mcp.tool()
def cancel_order(order_id: str, reason: str = "") -> dict:
    """Cancel an existing order.

    Args:
        order_id: The order to cancel.
        reason: Optional cancellation reason.

    Returns:
        Cancellation confirmation.
    """
    logger.info(f"--- ❌ cancel_order {order_id} ---")
    order = ORDERS.get(order_id)
    if not order:
        return {"error": f"Order {order_id} not found"}
    if order["status"] in ("delivered", "cancelled"):
        return {"error": f"Cannot cancel order in '{order['status']}' status"}
    order["status"] = "cancelled"
    order["cancel_reason"] = reason
    return {"status": "cancelled", "order": order}


@mcp.tool()
def get_order_history(customer_id: str, limit: int = 20) -> dict:
    """Get order history for a customer.

    Args:
        customer_id: The customer ID to look up.
        limit: Maximum number of orders to return.

    Returns:
        List of orders for the customer.
    """
    logger.info(f"--- 📋 get_order_history for {customer_id} ---")
    orders = [o for o in ORDERS.values() if o["customer_id"] == customer_id]
    orders.sort(key=lambda x: x["created_at"], reverse=True)
    return {"customer_id": customer_id, "orders": orders[:limit], "count": len(orders)}


if __name__ == "__main__":
    port = int(os.getenv("ORDER_MCP_PORT", "9002"))
    logger.info(f"📦 Order Engine MCP starting on port {port}")
    asyncio.run(mcp.run_async(transport="sse", host="0.0.0.0", port=port))
