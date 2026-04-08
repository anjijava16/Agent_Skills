"""FastMCP Server #9 — Analytics & Reporting (port 9009).

Tools for sales summaries, top products, revenue reports, and metrics.
"""

import asyncio
import logging
import os
from typing import Optional

from fastmcp import FastMCP

logger = logging.getLogger(__name__)
logging.basicConfig(format="[%(levelname)s]: %(message)s", level=logging.INFO)

mcp = FastMCP("Analytics & Reporting MCP Server 📊")

# ---------------------------------------------------------------------------
# Simulated analytics data
# ---------------------------------------------------------------------------

SALES_DATA = {
    "2025-01": {"month": "2025-01", "total_orders": 342, "total_revenue": 48560.00, "avg_order_value": 142.00, "returns": 18},
    "2024-12": {"month": "2024-12", "total_orders": 510, "total_revenue": 72300.00, "avg_order_value": 141.76, "returns": 25},
    "2024-11": {"month": "2024-11", "total_orders": 620, "total_revenue": 93100.00, "avg_order_value": 150.16, "returns": 31},
}

TOP_PRODUCTS = [
    {"sku": "SKU-1001", "name": "Wireless Headphones", "units_sold": 124, "revenue": 12375.76},
    {"sku": "SKU-1003", "name": "Blender Pro 3000", "units_sold": 98, "revenue": 4361.02},
    {"sku": "SKU-1002", "name": "Cotton T-Shirt", "units_sold": 210, "revenue": 5249.90},
    {"sku": "SKU-1004", "name": "Organic Granola", "units_sold": 340, "revenue": 2713.60},
    {"sku": "SKU-1005", "name": "Yoga Mat Premium", "units_sold": 72, "revenue": 2879.28},
]

CUSTOMER_METRICS = {
    "total_customers": 1520,
    "new_this_month": 87,
    "active_30d": 430,
    "churn_rate_pct": 3.2,
    "avg_lifetime_value": 285.50,
    "top_tier_distribution": {"bronze": 820, "silver": 450, "gold": 200, "platinum": 50},
}

INVENTORY_TURNOVER = [
    {"sku": "SKU-1001", "name": "Wireless Headphones", "turnover_rate": 4.2, "days_of_supply": 12},
    {"sku": "SKU-1002", "name": "Cotton T-Shirt", "turnover_rate": 6.8, "days_of_supply": 8},
    {"sku": "SKU-1003", "name": "Blender Pro 3000", "turnover_rate": 2.1, "days_of_supply": 25},
    {"sku": "SKU-1004", "name": "Organic Granola", "turnover_rate": 9.5, "days_of_supply": 5},
    {"sku": "SKU-1005", "name": "Yoga Mat Premium", "turnover_rate": 1.5, "days_of_supply": 40},
]


@mcp.tool()
def get_sales_summary(month: Optional[str] = None) -> dict:
    """Get a monthly sales summary.

    Args:
        month: Month in YYYY-MM format (omit for latest).

    Returns:
        Sales summary with orders, revenue, and returns.
    """
    logger.info(f"--- 📊 get_sales_summary month={month} ---")
    if month:
        data = SALES_DATA.get(month)
        if not data:
            return {"error": f"No data for month {month}"}
        return data
    return {"months": list(SALES_DATA.values()), "count": len(SALES_DATA)}


@mcp.tool()
def get_top_products(limit: int = 5, sort_by: str = "revenue") -> dict:
    """Get top-selling products.

    Args:
        limit: Number of products to return.
        sort_by: Sort criterion — 'revenue' or 'units_sold'.

    Returns:
        Ranked product list.
    """
    logger.info(f"--- 🏆 get_top_products limit={limit} sort={sort_by} ---")
    if sort_by not in ("revenue", "units_sold"):
        return {"error": f"Invalid sort_by: {sort_by}"}
    sorted_products = sorted(TOP_PRODUCTS, key=lambda p: p[sort_by], reverse=True)
    return {"top_products": sorted_products[:limit], "sorted_by": sort_by}


@mcp.tool()
def get_revenue_report(start_month: str = "2024-11", end_month: str = "2025-01") -> dict:
    """Get a revenue trend report across months.

    Args:
        start_month: Start month (YYYY-MM).
        end_month: End month (YYYY-MM).

    Returns:
        Monthly revenue trend and totals.
    """
    logger.info(f"--- 💰 get_revenue_report {start_month} to {end_month} ---")
    months = sorted(SALES_DATA.keys())
    filtered = [SALES_DATA[m] for m in months if start_month <= m <= end_month]
    total_rev = sum(m["total_revenue"] for m in filtered)
    total_orders = sum(m["total_orders"] for m in filtered)
    return {
        "period": f"{start_month} to {end_month}",
        "months": filtered,
        "total_revenue": round(total_rev, 2),
        "total_orders": total_orders,
        "avg_monthly_revenue": round(total_rev / max(len(filtered), 1), 2),
    }


@mcp.tool()
def get_customer_metrics() -> dict:
    """Get customer analytics metrics.

    Returns:
        Customer counts, churn rate, lifetime value, and tier distribution.
    """
    logger.info("--- 👥 get_customer_metrics ---")
    return CUSTOMER_METRICS


@mcp.tool()
def get_inventory_turnover(min_turnover: float = 0.0) -> dict:
    """Get inventory turnover rates for products.

    Args:
        min_turnover: Minimum turnover rate filter.

    Returns:
        Products with turnover rate and days of supply.
    """
    logger.info(f"--- 🔄 get_inventory_turnover min={min_turnover} ---")
    filtered = [i for i in INVENTORY_TURNOVER if i["turnover_rate"] >= min_turnover]
    filtered.sort(key=lambda x: x["turnover_rate"], reverse=True)
    return {"inventory_turnover": filtered, "count": len(filtered)}


if __name__ == "__main__":
    port = int(os.getenv("ANALYTICS_MCP_PORT", "9009"))
    logger.info(f"📊 Analytics MCP starting on port {port}")
    asyncio.run(mcp.run_async(transport="sse", host="0.0.0.0", port=port))
