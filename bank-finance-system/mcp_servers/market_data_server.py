"""MCP Server #7 — Market Data.

Provides tools for stock prices, portfolio management, and trading.
"""

import json
import uuid
from datetime import datetime
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

server = Server("market-data-mcp")

STOCKS: dict[str, dict] = {
    "AAPL": {"symbol": "AAPL", "name": "Apple Inc.", "price": 189.50, "change": 2.30, "change_pct": 1.23},
    "GOOGL": {"symbol": "GOOGL", "name": "Alphabet Inc.", "price": 141.80, "change": -0.90, "change_pct": -0.63},
    "MSFT": {"symbol": "MSFT", "name": "Microsoft Corp.", "price": 415.20, "change": 5.10, "change_pct": 1.24},
    "AMZN": {"symbol": "AMZN", "name": "Amazon.com Inc.", "price": 185.60, "change": 3.40, "change_pct": 1.87},
    "TSLA": {"symbol": "TSLA", "name": "Tesla Inc.", "price": 248.90, "change": -4.20, "change_pct": -1.66},
}

PORTFOLIOS: dict[str, list[dict]] = {
    "ACC-1001": [
        {"symbol": "AAPL", "quantity": 50, "avg_price": 175.00},
        {"symbol": "MSFT", "quantity": 20, "avg_price": 380.00},
    ],
    "ACC-1003": [
        {"symbol": "GOOGL", "quantity": 100, "avg_price": 130.00},
        {"symbol": "AMZN", "quantity": 30, "avg_price": 170.00},
        {"symbol": "TSLA", "quantity": 15, "avg_price": 220.00},
    ],
}


@server.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="get_stock_price",
            description="Get the current price and daily change for a stock.",
            inputSchema={
                "type": "object",
                "properties": {"symbol": {"type": "string", "description": "Stock ticker symbol (e.g. AAPL)"}},
                "required": ["symbol"],
            },
        ),
        Tool(
            name="get_portfolio",
            description="Get the investment portfolio for an account.",
            inputSchema={
                "type": "object",
                "properties": {"account_id": {"type": "string", "description": "Account ID"}},
                "required": ["account_id"],
            },
        ),
        Tool(
            name="buy_stock",
            description="Buy shares of a stock.",
            inputSchema={
                "type": "object",
                "properties": {
                    "account_id": {"type": "string", "description": "Account ID"},
                    "symbol": {"type": "string", "description": "Stock symbol"},
                    "quantity": {"type": "integer", "description": "Number of shares to buy"},
                },
                "required": ["account_id", "symbol", "quantity"],
            },
        ),
        Tool(
            name="sell_stock",
            description="Sell shares of a stock from the portfolio.",
            inputSchema={
                "type": "object",
                "properties": {
                    "account_id": {"type": "string", "description": "Account ID"},
                    "symbol": {"type": "string", "description": "Stock symbol"},
                    "quantity": {"type": "integer", "description": "Number of shares to sell"},
                },
                "required": ["account_id", "symbol", "quantity"],
            },
        ),
        Tool(
            name="get_market_summary",
            description="Get a summary of major market indices and top movers.",
            inputSchema={"type": "object", "properties": {}},
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    if name == "get_stock_price":
        symbol = arguments["symbol"].upper()
        stock = STOCKS.get(symbol)
        if not stock:
            return [TextContent(type="text", text=json.dumps({"error": f"Stock {symbol} not found"}))]
        return [TextContent(type="text", text=json.dumps(stock))]

    elif name == "get_portfolio":
        account_id = arguments["account_id"]
        holdings = PORTFOLIOS.get(account_id, [])
        enriched = []
        total_value = 0.0
        total_cost = 0.0
        for h in holdings:
            stock = STOCKS.get(h["symbol"], {})
            current_price = stock.get("price", 0)
            market_value = current_price * h["quantity"]
            cost_basis = h["avg_price"] * h["quantity"]
            total_value += market_value
            total_cost += cost_basis
            enriched.append({
                **h,
                "current_price": current_price,
                "market_value": round(market_value, 2),
                "gain_loss": round(market_value - cost_basis, 2),
            })
        return [TextContent(type="text", text=json.dumps({
            "account_id": account_id,
            "holdings": enriched,
            "total_value": round(total_value, 2),
            "total_gain_loss": round(total_value - total_cost, 2),
        }))]

    elif name == "buy_stock":
        symbol = arguments["symbol"].upper()
        stock = STOCKS.get(symbol)
        if not stock:
            return [TextContent(type="text", text=json.dumps({"error": f"Stock {symbol} not found"}))]
        account_id = arguments["account_id"]
        portfolio = PORTFOLIOS.setdefault(account_id, [])
        existing = next((h for h in portfolio if h["symbol"] == symbol), None)
        price = stock["price"]
        qty = arguments["quantity"]
        if existing:
            total_cost = existing["avg_price"] * existing["quantity"] + price * qty
            existing["quantity"] += qty
            existing["avg_price"] = round(total_cost / existing["quantity"], 2)
        else:
            portfolio.append({"symbol": symbol, "quantity": qty, "avg_price": price})
        return [TextContent(type="text", text=json.dumps({
            "status": "bought",
            "symbol": symbol,
            "quantity": qty,
            "price": price,
            "total_cost": round(price * qty, 2),
        }))]

    elif name == "sell_stock":
        symbol = arguments["symbol"].upper()
        account_id = arguments["account_id"]
        portfolio = PORTFOLIOS.get(account_id, [])
        existing = next((h for h in portfolio if h["symbol"] == symbol), None)
        if not existing or existing["quantity"] < arguments["quantity"]:
            return [TextContent(type="text", text=json.dumps({"error": "Insufficient shares to sell"}))]
        stock = STOCKS.get(symbol, {})
        price = stock.get("price", 0)
        qty = arguments["quantity"]
        existing["quantity"] -= qty
        if existing["quantity"] == 0:
            portfolio.remove(existing)
        return [TextContent(type="text", text=json.dumps({
            "status": "sold",
            "symbol": symbol,
            "quantity": qty,
            "price": price,
            "total_proceeds": round(price * qty, 2),
        }))]

    elif name == "get_market_summary":
        top_gainers = sorted(STOCKS.values(), key=lambda s: s["change_pct"], reverse=True)[:3]
        top_losers = sorted(STOCKS.values(), key=lambda s: s["change_pct"])[:2]
        return [TextContent(type="text", text=json.dumps({
            "market_status": "open",
            "top_gainers": top_gainers,
            "top_losers": top_losers,
            "timestamp": datetime.utcnow().isoformat() + "Z",
        }))]

    return [TextContent(type="text", text=json.dumps({"error": f"Unknown tool: {name}"}))]


async def main():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
