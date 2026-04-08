"""FastMCP Server #4 — Customer Database (port 9004).

Tools for customer profiles, loyalty points, preferences, and search.
"""

import asyncio
import logging
import os
import uuid
from typing import Optional

from fastmcp import FastMCP

logger = logging.getLogger(__name__)
logging.basicConfig(format="[%(levelname)s]: %(message)s", level=logging.INFO)

mcp = FastMCP("Customer Database MCP Server 👤")

# ---------------------------------------------------------------------------
# In-memory customer store
# ---------------------------------------------------------------------------

CUSTOMERS = {
    "CUST-100": {
        "customer_id": "CUST-100",
        "name": "Alice Johnson",
        "email": "alice@example.com",
        "phone": "+1-555-0100",
        "tier": "gold",
        "loyalty_points": 2450,
        "preferences": {"notifications": True, "preferred_category": "CAT-ELEC"},
        "status": "active",
    },
    "CUST-101": {
        "customer_id": "CUST-101",
        "name": "Bob Smith",
        "email": "bob@example.com",
        "phone": "+1-555-0101",
        "tier": "silver",
        "loyalty_points": 820,
        "preferences": {"notifications": True, "preferred_category": "CAT-CLTH"},
        "status": "active",
    },
    "CUST-102": {
        "customer_id": "CUST-102",
        "name": "Carol Williams",
        "email": "carol@example.com",
        "phone": "+1-555-0102",
        "tier": "bronze",
        "loyalty_points": 150,
        "preferences": {"notifications": False, "preferred_category": "CAT-HOME"},
        "status": "active",
    },
}


@mcp.tool()
def get_customer(customer_id: str) -> dict:
    """Get full customer profile.

    Args:
        customer_id: The customer identifier (e.g., 'CUST-100').

    Returns:
        Customer profile details or error if not found.
    """
    logger.info(f"--- 👤 get_customer {customer_id} ---")
    customer = CUSTOMERS.get(customer_id)
    if not customer:
        return {"error": f"Customer {customer_id} not found"}
    return customer


@mcp.tool()
def create_customer(
    name: str,
    email: str,
    phone: str = "",
) -> dict:
    """Register a new customer.

    Args:
        name: Customer full name.
        email: Customer email address.
        phone: Customer phone number (optional).

    Returns:
        The created customer profile with assigned ID.
    """
    logger.info(f"--- ➕ create_customer: {name} ---")
    for c in CUSTOMERS.values():
        if c["email"] == email:
            return {"error": f"Email {email} already registered"}
    cid = f"CUST-{uuid.uuid4().hex[:3].upper()}"
    customer = {
        "customer_id": cid,
        "name": name,
        "email": email,
        "phone": phone,
        "tier": "bronze",
        "loyalty_points": 0,
        "preferences": {"notifications": True, "preferred_category": None},
        "status": "active",
    }
    CUSTOMERS[cid] = customer
    return {"status": "created", "customer": customer}


@mcp.tool()
def update_customer(
    customer_id: str,
    name: Optional[str] = None,
    email: Optional[str] = None,
    phone: Optional[str] = None,
    tier: Optional[str] = None,
) -> dict:
    """Update an existing customer's profile.

    Args:
        customer_id: Customer to update.
        name: New name (optional).
        email: New email (optional).
        phone: New phone (optional).
        tier: New loyalty tier — 'bronze', 'silver', 'gold', 'platinum' (optional).

    Returns:
        Updated customer profile.
    """
    logger.info(f"--- ✏️ update_customer {customer_id} ---")
    customer = CUSTOMERS.get(customer_id)
    if not customer:
        return {"error": f"Customer {customer_id} not found"}
    if name is not None:
        customer["name"] = name
    if email is not None:
        customer["email"] = email
    if phone is not None:
        customer["phone"] = phone
    if tier is not None:
        if tier not in ("bronze", "silver", "gold", "platinum"):
            return {"error": f"Invalid tier: {tier}"}
        customer["tier"] = tier
    return {"status": "updated", "customer": customer}


@mcp.tool()
def get_loyalty_points(customer_id: str) -> dict:
    """Check a customer's loyalty points balance and tier.

    Args:
        customer_id: Customer to check.

    Returns:
        Loyalty points, tier, and point value estimate.
    """
    logger.info(f"--- ⭐ get_loyalty_points {customer_id} ---")
    customer = CUSTOMERS.get(customer_id)
    if not customer:
        return {"error": f"Customer {customer_id} not found"}
    points = customer["loyalty_points"]
    return {
        "customer_id": customer_id,
        "name": customer["name"],
        "tier": customer["tier"],
        "loyalty_points": points,
        "point_value_usd": round(points * 0.01, 2),
    }


@mcp.tool()
def search_customers(
    query: str,
    tier: Optional[str] = None,
    limit: int = 10,
) -> dict:
    """Search customers by name or email.

    Args:
        query: Text to match against name or email.
        tier: Optional tier filter ('bronze', 'silver', 'gold', 'platinum').
        limit: Maximum results.

    Returns:
        Matching customer list.
    """
    logger.info(f"--- 🔎 search_customers: '{query}' ---")
    q = query.lower()
    results = []
    for c in CUSTOMERS.values():
        if c["status"] != "active":
            continue
        if q not in c["name"].lower() and q not in c["email"].lower():
            continue
        if tier and c["tier"] != tier:
            continue
        results.append(c)
        if len(results) >= limit:
            break
    return {"results": results, "count": len(results)}


if __name__ == "__main__":
    port = int(os.getenv("CUSTOMER_MCP_PORT", "9004"))
    logger.info(f"👤 Customer DB MCP starting on port {port}")
    asyncio.run(mcp.run_async(transport="sse", host="0.0.0.0", port=port))
