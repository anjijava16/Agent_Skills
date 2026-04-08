"""FastMCP Server #8 — Returns & Refunds (port 9008).

Tools for return requests, status tracking, approval, and refund processing.
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

mcp = FastMCP("Returns & Refunds MCP Server 🔁")

# ---------------------------------------------------------------------------
# In-memory returns store
# ---------------------------------------------------------------------------

RETURNS = {
    "RET-8001": {
        "return_id": "RET-8001",
        "order_id": "ORD-2001",
        "customer_id": "CUST-100",
        "items": [{"sku": "SKU-1001", "quantity": 1, "reason": "defective"}],
        "status": "completed",
        "refund_amount": 999.99,
        "refund_status": "refunded",
        "created_at": "2025-01-16T09:00:00Z",
        "resolved_at": "2025-01-18T14:00:00Z",
    },
}


@mcp.tool()
def initiate_return(
    order_id: str,
    customer_id: str,
    sku: str,
    quantity: int = 1,
    reason: str = "changed_mind",
) -> dict:
    """Initiate a return request for an order item.

    Args:
        order_id: Original order.
        customer_id: Customer requesting the return.
        sku: Product SKU to return.
        quantity: Number of units.
        reason: Reason — 'defective', 'wrong_item', 'changed_mind', 'not_as_described'.

    Returns:
        Return request confirmation with ID and instructions.
    """
    logger.info(f"--- 🔁 initiate_return ORD={order_id} SKU={sku} ---")
    valid_reasons = {"defective", "wrong_item", "changed_mind", "not_as_described"}
    if reason not in valid_reasons:
        return {"error": f"Invalid reason. Choose from: {valid_reasons}"}
    ret_id = f"RET-{uuid.uuid4().hex[:4].upper()}"
    ret = {
        "return_id": ret_id,
        "order_id": order_id,
        "customer_id": customer_id,
        "items": [{"sku": sku, "quantity": quantity, "reason": reason}],
        "status": "pending_review",
        "refund_amount": 0.0,
        "refund_status": "pending",
        "created_at": datetime.utcnow().isoformat() + "Z",
        "resolved_at": None,
    }
    RETURNS[ret_id] = ret
    return {
        "status": "return_initiated",
        "return_id": ret_id,
        "instructions": "Please ship the item back using the prepaid label within 14 days.",
    }


@mcp.tool()
def get_return_status(return_id: str) -> dict:
    """Check the status of a return request.

    Args:
        return_id: Return to look up.

    Returns:
        Return status details.
    """
    logger.info(f"--- 🔍 get_return_status {return_id} ---")
    ret = RETURNS.get(return_id)
    if not ret:
        return {"error": f"Return {return_id} not found"}
    return {
        "return_id": ret["return_id"],
        "order_id": ret["order_id"],
        "status": ret["status"],
        "refund_amount": ret["refund_amount"],
        "refund_status": ret["refund_status"],
        "items": ret["items"],
    }


@mcp.tool()
def approve_return(return_id: str, refund_amount: float) -> dict:
    """Approve a pending return and set refund amount.

    Args:
        return_id: Return to approve.
        refund_amount: Amount to refund.

    Returns:
        Approval confirmation.
    """
    logger.info(f"--- ✅ approve_return {return_id} refund=${refund_amount} ---")
    ret = RETURNS.get(return_id)
    if not ret:
        return {"error": f"Return {return_id} not found"}
    if ret["status"] not in ("pending_review", "item_received"):
        return {"error": f"Cannot approve return in status '{ret['status']}'"}
    ret["status"] = "approved"
    ret["refund_amount"] = refund_amount
    return {"status": "return_approved", "return_id": return_id, "refund_amount": refund_amount}


@mcp.tool()
def process_refund(return_id: str) -> dict:
    """Process refund for an approved return.

    Args:
        return_id: Approved return to refund.

    Returns:
        Refund processing confirmation.
    """
    logger.info(f"--- 💰 process_refund {return_id} ---")
    ret = RETURNS.get(return_id)
    if not ret:
        return {"error": f"Return {return_id} not found"}
    if ret["status"] != "approved":
        return {"error": f"Return must be approved first (current: {ret['status']})"}
    ret["status"] = "completed"
    ret["refund_status"] = "refunded"
    ret["resolved_at"] = datetime.utcnow().isoformat() + "Z"
    return {
        "status": "refund_processed",
        "return_id": return_id,
        "refund_amount": ret["refund_amount"],
        "refund_status": "refunded",
    }


@mcp.tool()
def list_returns(
    customer_id: Optional[str] = None,
    status: Optional[str] = None,
    limit: int = 20,
) -> dict:
    """List return requests with optional filters.

    Args:
        customer_id: Filter by customer (optional).
        status: Filter by status (optional).
        limit: Max results.

    Returns:
        Matching return requests.
    """
    logger.info(f"--- 📋 list_returns cust={customer_id} status={status} ---")
    results = []
    for r in RETURNS.values():
        if customer_id and r["customer_id"] != customer_id:
            continue
        if status and r["status"] != status:
            continue
        results.append(r)
        if len(results) >= limit:
            break
    return {"returns": results, "count": len(results)}


if __name__ == "__main__":
    port = int(os.getenv("RETURNS_MCP_PORT", "9008"))
    logger.info(f"🔁 Returns MCP starting on port {port}")
    asyncio.run(mcp.run_async(transport="sse", host="0.0.0.0", port=port))
