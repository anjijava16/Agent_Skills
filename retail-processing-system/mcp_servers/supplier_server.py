"""FastMCP Server #10 — Supplier Management (port 9010).

Tools for supplier profiles, purchase orders, and supply-chain operations.
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

mcp = FastMCP("Supplier Management MCP Server 🏭")

# ---------------------------------------------------------------------------
# In-memory supplier & PO stores
# ---------------------------------------------------------------------------

SUPPLIERS = {
    "SUP-300": {
        "supplier_id": "SUP-300",
        "name": "TechSource Electronics",
        "contact_email": "sales@techsource.com",
        "phone": "+1-555-3000",
        "categories": ["CAT-ELEC"],
        "lead_time_days": 7,
        "rating": 4.5,
        "status": "active",
    },
    "SUP-301": {
        "supplier_id": "SUP-301",
        "name": "FreshGoods Inc.",
        "contact_email": "orders@freshgoods.com",
        "phone": "+1-555-3010",
        "categories": ["CAT-GROC"],
        "lead_time_days": 3,
        "rating": 4.2,
        "status": "active",
    },
    "SUP-302": {
        "supplier_id": "SUP-302",
        "name": "HomeStyle Manufacturing",
        "contact_email": "wholesale@homestyle.com",
        "phone": "+1-555-3020",
        "categories": ["CAT-HOME", "CAT-SPRT"],
        "lead_time_days": 14,
        "rating": 3.8,
        "status": "active",
    },
}

PURCHASE_ORDERS = {
    "PO-4001": {
        "po_id": "PO-4001",
        "supplier_id": "SUP-300",
        "items": [{"sku": "SKU-1001", "quantity": 200, "unit_cost": 55.00}],
        "total_cost": 11000.00,
        "status": "delivered",
        "ordered_at": "2025-01-05T10:00:00Z",
        "expected_delivery": "2025-01-12",
        "delivered_at": "2025-01-11T16:00:00Z",
    },
    "PO-4002": {
        "po_id": "PO-4002",
        "supplier_id": "SUP-301",
        "items": [{"sku": "SKU-1004", "quantity": 500, "unit_cost": 4.50}],
        "total_cost": 2250.00,
        "status": "in_transit",
        "ordered_at": "2025-01-13T08:00:00Z",
        "expected_delivery": "2025-01-16",
        "delivered_at": None,
    },
}


@mcp.tool()
def get_supplier(supplier_id: str) -> dict:
    """Get supplier profile and details.

    Args:
        supplier_id: Supplier identifier (e.g., 'SUP-300').

    Returns:
        Full supplier profile.
    """
    logger.info(f"--- 🏭 get_supplier {supplier_id} ---")
    supplier = SUPPLIERS.get(supplier_id)
    if not supplier:
        return {"error": f"Supplier {supplier_id} not found"}
    return supplier


@mcp.tool()
def create_purchase_order(
    supplier_id: str,
    sku: str,
    quantity: int,
    unit_cost: float,
) -> dict:
    """Create a purchase order to a supplier.

    Args:
        supplier_id: Supplier to order from.
        sku: Product SKU to order.
        quantity: Number of units.
        unit_cost: Cost per unit.

    Returns:
        Purchase order confirmation.
    """
    logger.info(f"--- 📝 create_purchase_order SUP={supplier_id} SKU={sku} qty={quantity} ---")
    supplier = SUPPLIERS.get(supplier_id)
    if not supplier:
        return {"error": f"Supplier {supplier_id} not found"}
    if supplier["status"] != "active":
        return {"error": "Supplier is not active"}
    po_id = f"PO-{uuid.uuid4().hex[:4].upper()}"
    total = round(quantity * unit_cost, 2)
    po = {
        "po_id": po_id,
        "supplier_id": supplier_id,
        "items": [{"sku": sku, "quantity": quantity, "unit_cost": unit_cost}],
        "total_cost": total,
        "status": "submitted",
        "ordered_at": datetime.utcnow().isoformat() + "Z",
        "expected_delivery": "",
        "delivered_at": None,
    }
    PURCHASE_ORDERS[po_id] = po
    return {"status": "po_created", "purchase_order": po}


@mcp.tool()
def get_po_status(po_id: str) -> dict:
    """Check the status of a purchase order.

    Args:
        po_id: Purchase order identifier.

    Returns:
        PO status and delivery info.
    """
    logger.info(f"--- 🔍 get_po_status {po_id} ---")
    po = PURCHASE_ORDERS.get(po_id)
    if not po:
        return {"error": f"Purchase order {po_id} not found"}
    return {
        "po_id": po["po_id"],
        "supplier": SUPPLIERS.get(po["supplier_id"], {}).get("name", "Unknown"),
        "status": po["status"],
        "total_cost": po["total_cost"],
        "expected_delivery": po["expected_delivery"],
        "delivered_at": po["delivered_at"],
    }


@mcp.tool()
def list_suppliers(category: Optional[str] = None, min_rating: float = 0.0) -> dict:
    """List suppliers with optional filters.

    Args:
        category: Filter by supply category (optional).
        min_rating: Minimum rating filter.

    Returns:
        Matching suppliers.
    """
    logger.info(f"--- 📋 list_suppliers cat={category} min_rating={min_rating} ---")
    results = []
    for s in SUPPLIERS.values():
        if s["status"] != "active":
            continue
        if s["rating"] < min_rating:
            continue
        if category and category not in s["categories"]:
            continue
        results.append(s)
    return {"suppliers": results, "count": len(results)}


@mcp.tool()
def update_supplier(
    supplier_id: str,
    name: Optional[str] = None,
    contact_email: Optional[str] = None,
    phone: Optional[str] = None,
    rating: Optional[float] = None,
    status: Optional[str] = None,
) -> dict:
    """Update a supplier profile.

    Args:
        supplier_id: Supplier to update.
        name: New name (optional).
        contact_email: New email (optional).
        phone: New phone (optional).
        rating: New rating 0-5 (optional).
        status: New status — 'active' or 'inactive' (optional).

    Returns:
        Updated supplier profile.
    """
    logger.info(f"--- ✏️ update_supplier {supplier_id} ---")
    supplier = SUPPLIERS.get(supplier_id)
    if not supplier:
        return {"error": f"Supplier {supplier_id} not found"}
    if name is not None:
        supplier["name"] = name
    if contact_email is not None:
        supplier["contact_email"] = contact_email
    if phone is not None:
        supplier["phone"] = phone
    if rating is not None:
        if not (0 <= rating <= 5):
            return {"error": "Rating must be 0-5"}
        supplier["rating"] = rating
    if status is not None:
        if status not in ("active", "inactive"):
            return {"error": f"Invalid status: {status}"}
        supplier["status"] = status
    return {"status": "updated", "supplier": supplier}


if __name__ == "__main__":
    port = int(os.getenv("SUPPLIER_MCP_PORT", "9010"))
    logger.info(f"🏭 Supplier MCP starting on port {port}")
    asyncio.run(mcp.run_async(transport="sse", host="0.0.0.0", port=port))
