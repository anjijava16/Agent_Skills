"""FastMCP Server #1 — Product Catalog (port 9001).

Tools for product search, details, categories, and CRUD.
"""

import asyncio
import logging
import os
import json
import uuid
from typing import Optional

from fastmcp import FastMCP

logger = logging.getLogger(__name__)
logging.basicConfig(format="[%(levelname)s]: %(message)s", level=logging.INFO)

mcp = FastMCP("Product Catalog MCP Server 🛍️")

# ---------------------------------------------------------------------------
# In-memory product store
# ---------------------------------------------------------------------------

CATEGORIES = {
    "CAT-ELEC": {"name": "Electronics", "description": "Gadgets, phones, laptops"},
    "CAT-CLTH": {"name": "Clothing", "description": "Apparel, shoes, accessories"},
    "CAT-HOME": {"name": "Home & Kitchen", "description": "Furniture, appliances, décor"},
    "CAT-FOOD": {"name": "Grocery & Food", "description": "Packaged food, beverages, snacks"},
    "CAT-SPRT": {"name": "Sports & Outdoors", "description": "Fitness, camping, gear"},
}

PRODUCTS = {
    "SKU-1001": {
        "sku": "SKU-1001",
        "name": "Wireless Bluetooth Headphones",
        "category": "CAT-ELEC",
        "price": 79.99,
        "description": "Noise-cancelling over-ear headphones with 30h battery",
        "status": "active",
    },
    "SKU-1002": {
        "sku": "SKU-1002",
        "name": "Organic Cotton T-Shirt",
        "category": "CAT-CLTH",
        "price": 24.99,
        "description": "100% organic cotton, available in S/M/L/XL",
        "status": "active",
    },
    "SKU-1003": {
        "sku": "SKU-1003",
        "name": "Stainless Steel Water Bottle",
        "category": "CAT-SPRT",
        "price": 18.50,
        "description": "750ml insulated bottle, keeps drinks cold 24h",
        "status": "active",
    },
    "SKU-1004": {
        "sku": "SKU-1004",
        "name": "Smart LED Desk Lamp",
        "category": "CAT-HOME",
        "price": 45.00,
        "description": "Adjustable brightness and color temperature, USB charging",
        "status": "active",
    },
    "SKU-1005": {
        "sku": "SKU-1005",
        "name": "Trail Mix Variety Pack",
        "category": "CAT-FOOD",
        "price": 12.99,
        "description": "12-pack assorted trail mix, no artificial flavors",
        "status": "active",
    },
}


# ---------------------------------------------------------------------------
# Tools
# ---------------------------------------------------------------------------


@mcp.tool()
def get_product(sku: str) -> dict:
    """Get full product details by SKU.

    Args:
        sku: The product SKU identifier (e.g., 'SKU-1001').

    Returns:
        Product details or error if not found.
    """
    logger.info(f"--- 🔍 get_product called for {sku} ---")
    product = PRODUCTS.get(sku)
    if not product:
        return {"error": f"Product {sku} not found"}
    return product


@mcp.tool()
def search_products(
    query: str,
    category: Optional[str] = None,
    max_price: Optional[float] = None,
    limit: int = 10,
) -> dict:
    """Search products by name/description with optional filters.

    Args:
        query: Search text to match against product name or description.
        category: Optional category ID to filter by (e.g., 'CAT-ELEC').
        max_price: Optional maximum price filter.
        limit: Maximum results to return.

    Returns:
        List of matching products.
    """
    logger.info(f"--- 🔎 search_products called: query='{query}' ---")
    results = []
    q = query.lower()
    for p in PRODUCTS.values():
        if p["status"] != "active":
            continue
        if q not in p["name"].lower() and q not in p["description"].lower():
            continue
        if category and p["category"] != category:
            continue
        if max_price and p["price"] > max_price:
            continue
        results.append(p)
        if len(results) >= limit:
            break
    return {"results": results, "count": len(results), "query": query}


@mcp.tool()
def list_categories() -> dict:
    """List all product categories.

    Returns:
        All available product categories.
    """
    logger.info("--- 📋 list_categories called ---")
    return {"categories": CATEGORIES, "count": len(CATEGORIES)}


@mcp.tool()
def create_product(
    name: str,
    category: str,
    price: float,
    description: str,
) -> dict:
    """Create a new product in the catalog.

    Args:
        name: Product display name.
        category: Category ID (e.g., 'CAT-ELEC').
        price: Product price in USD.
        description: Short product description.

    Returns:
        The created product with assigned SKU.
    """
    logger.info(f"--- ➕ create_product called: {name} ---")
    if category not in CATEGORIES:
        return {"error": f"Unknown category: {category}"}
    sku = f"SKU-{uuid.uuid4().hex[:4].upper()}"
    product = {
        "sku": sku,
        "name": name,
        "category": category,
        "price": round(price, 2),
        "description": description,
        "status": "active",
    }
    PRODUCTS[sku] = product
    return {"status": "created", "product": product}


@mcp.tool()
def update_product(
    sku: str,
    name: Optional[str] = None,
    price: Optional[float] = None,
    description: Optional[str] = None,
    status: Optional[str] = None,
) -> dict:
    """Update an existing product's details.

    Args:
        sku: The product SKU to update.
        name: New product name (optional).
        price: New price (optional).
        description: New description (optional).
        status: New status — 'active' or 'discontinued' (optional).

    Returns:
        Updated product details.
    """
    logger.info(f"--- ✏️ update_product called for {sku} ---")
    product = PRODUCTS.get(sku)
    if not product:
        return {"error": f"Product {sku} not found"}
    if name is not None:
        product["name"] = name
    if price is not None:
        product["price"] = round(price, 2)
    if description is not None:
        product["description"] = description
    if status is not None:
        product["status"] = status
    return {"status": "updated", "product": product}


# ---------------------------------------------------------------------------
# Server startup
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    port = int(os.getenv("PRODUCT_MCP_PORT", "9001"))
    logger.info(f"🛍️ Product Catalog MCP starting on port {port}")
    asyncio.run(mcp.run_async(transport="sse", host="0.0.0.0", port=port))
