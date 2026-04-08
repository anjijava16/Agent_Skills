"""FastMCP Server #7 — Promotions & Pricing (port 9007).

Tools for coupons, active promotions, discount calculation, and validation.
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

mcp = FastMCP("Promotions & Pricing MCP Server 🏷️")

# ---------------------------------------------------------------------------
# In-memory promotion / coupon stores
# ---------------------------------------------------------------------------

PROMOTIONS = {
    "PROMO-001": {
        "promo_id": "PROMO-001",
        "name": "New Year Sale",
        "type": "percentage",
        "value": 15.0,
        "min_order": 50.0,
        "applicable_categories": ["CAT-ELEC", "CAT-HOME"],
        "start_date": "2025-01-01",
        "end_date": "2025-01-31",
        "active": True,
    },
    "PROMO-002": {
        "promo_id": "PROMO-002",
        "name": "Free Shipping Week",
        "type": "free_shipping",
        "value": 0,
        "min_order": 25.0,
        "applicable_categories": [],
        "start_date": "2025-01-15",
        "end_date": "2025-01-22",
        "active": True,
    },
}

COUPONS = {
    "SAVE10": {"code": "SAVE10", "promo_id": "PROMO-001", "max_uses": 100, "used": 12, "single_use_per_customer": True},
    "FREESHIP": {"code": "FREESHIP", "promo_id": "PROMO-002", "max_uses": 500, "used": 87, "single_use_per_customer": False},
}


@mcp.tool()
def apply_coupon(code: str, order_total: float, category: str = "") -> dict:
    """Apply a coupon code to calculate the discount.

    Args:
        code: Coupon code (e.g., 'SAVE10').
        order_total: Cart total before discount.
        category: Primary category of the order (optional, for eligibility).

    Returns:
        Discount amount and new total, or error if invalid.
    """
    logger.info(f"--- 🎟️ apply_coupon code={code} total=${order_total} ---")
    coupon = COUPONS.get(code.upper())
    if not coupon:
        return {"error": f"Coupon '{code}' not found"}
    if coupon["used"] >= coupon["max_uses"]:
        return {"error": "Coupon has reached maximum uses"}
    promo = PROMOTIONS.get(coupon["promo_id"])
    if not promo or not promo["active"]:
        return {"error": "Associated promotion is inactive"}
    if order_total < promo["min_order"]:
        return {"error": f"Minimum order ${promo['min_order']} not met"}
    if promo["applicable_categories"] and category and category not in promo["applicable_categories"]:
        return {"error": f"Coupon not applicable to category {category}"}

    discount = 0.0
    if promo["type"] == "percentage":
        discount = round(order_total * promo["value"] / 100, 2)
    elif promo["type"] == "fixed":
        discount = min(promo["value"], order_total)
    elif promo["type"] == "free_shipping":
        discount = 0.0  # handled at checkout level

    coupon["used"] += 1
    return {
        "code": code,
        "promo_name": promo["name"],
        "discount_type": promo["type"],
        "discount_amount": discount,
        "original_total": order_total,
        "new_total": round(order_total - discount, 2),
    }


@mcp.tool()
def get_active_promotions() -> dict:
    """Get all currently active promotions.

    Returns:
        List of active promotions with details.
    """
    logger.info("--- 📢 get_active_promotions ---")
    active = [p for p in PROMOTIONS.values() if p["active"]]
    return {"promotions": active, "count": len(active)}


@mcp.tool()
def calculate_discount(
    order_total: float,
    promo_id: str,
) -> dict:
    """Calculate the discount for a specific promotion without redeeming.

    Args:
        order_total: Cart total.
        promo_id: Promotion identifier.

    Returns:
        Calculated discount preview.
    """
    logger.info(f"--- 🧮 calculate_discount promo={promo_id} total=${order_total} ---")
    promo = PROMOTIONS.get(promo_id)
    if not promo:
        return {"error": f"Promotion {promo_id} not found"}
    if not promo["active"]:
        return {"error": "Promotion is inactive"}
    if order_total < promo["min_order"]:
        return {"eligible": False, "reason": f"Minimum order ${promo['min_order']} not met"}
    discount = 0.0
    if promo["type"] == "percentage":
        discount = round(order_total * promo["value"] / 100, 2)
    elif promo["type"] == "fixed":
        discount = min(promo["value"], order_total)
    return {
        "promo_id": promo_id,
        "promo_name": promo["name"],
        "eligible": True,
        "discount_amount": discount,
        "estimated_total": round(order_total - discount, 2),
    }


@mcp.tool()
def create_promotion(
    name: str,
    promo_type: str,
    value: float,
    min_order: float = 0.0,
    start_date: str = "",
    end_date: str = "",
) -> dict:
    """Create a new promotion.

    Args:
        name: Promotion name.
        promo_type: Type — 'percentage', 'fixed', 'free_shipping'.
        value: Discount value (percentage or dollar amount).
        min_order: Minimum order amount.
        start_date: Start date (YYYY-MM-DD).
        end_date: End date (YYYY-MM-DD).

    Returns:
        Created promotion details.
    """
    logger.info(f"--- ➕ create_promotion: {name} ---")
    if promo_type not in ("percentage", "fixed", "free_shipping"):
        return {"error": f"Invalid type: {promo_type}"}
    pid = f"PROMO-{uuid.uuid4().hex[:3].upper()}"
    promo = {
        "promo_id": pid,
        "name": name,
        "type": promo_type,
        "value": value,
        "min_order": min_order,
        "applicable_categories": [],
        "start_date": start_date or datetime.utcnow().strftime("%Y-%m-%d"),
        "end_date": end_date or "",
        "active": True,
    }
    PROMOTIONS[pid] = promo
    return {"status": "created", "promotion": promo}


@mcp.tool()
def validate_coupon(code: str) -> dict:
    """Validate whether a coupon code is usable.

    Args:
        code: Coupon code to validate.

    Returns:
        Validity status with remaining uses.
    """
    logger.info(f"--- ✅ validate_coupon code={code} ---")
    coupon = COUPONS.get(code.upper())
    if not coupon:
        return {"valid": False, "reason": "Coupon not found"}
    promo = PROMOTIONS.get(coupon["promo_id"])
    if not promo or not promo["active"]:
        return {"valid": False, "reason": "Associated promotion inactive"}
    remaining = coupon["max_uses"] - coupon["used"]
    if remaining <= 0:
        return {"valid": False, "reason": "No uses remaining"}
    return {
        "valid": True,
        "code": code,
        "promo_name": promo["name"],
        "discount_type": promo["type"],
        "discount_value": promo["value"],
        "remaining_uses": remaining,
    }


if __name__ == "__main__":
    port = int(os.getenv("PROMOTIONS_MCP_PORT", "9007"))
    logger.info(f"🏷️ Promotions MCP starting on port {port}")
    asyncio.run(mcp.run_async(transport="sse", host="0.0.0.0", port=port))
