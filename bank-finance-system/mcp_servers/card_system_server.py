"""MCP Server #4 — Card System.

Provides tools for credit/debit card issuance, blocking, limits, and rewards.
"""

import json
import uuid
from datetime import datetime
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

server = Server("card-system-mcp")

CARDS: dict[str, dict] = {
    "CARD-3001": {
        "card_id": "CARD-3001",
        "account_id": "ACC-1001",
        "card_type": "credit",
        "card_number": "****-****-****-4521",
        "credit_limit": 10000.00,
        "available_limit": 7500.00,
        "rewards_points": 2500,
        "status": "active",
        "issued_at": "2024-01-20T00:00:00Z",
    },
    "CARD-3002": {
        "card_id": "CARD-3002",
        "account_id": "ACC-1002",
        "card_type": "debit",
        "card_number": "****-****-****-8832",
        "daily_limit": 5000.00,
        "rewards_points": 800,
        "status": "active",
        "issued_at": "2024-03-25T00:00:00Z",
    },
}


@server.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="issue_card",
            description="Issue a new credit or debit card for an account.",
            inputSchema={
                "type": "object",
                "properties": {
                    "account_id": {"type": "string", "description": "Account ID to link the card"},
                    "card_type": {"type": "string", "enum": ["credit", "debit"], "description": "Type of card"},
                    "credit_limit": {"type": "number", "description": "Credit limit (for credit cards only)"},
                },
                "required": ["account_id", "card_type"],
            },
        ),
        Tool(
            name="block_card",
            description="Block a card immediately (lost/stolen/fraud).",
            inputSchema={
                "type": "object",
                "properties": {
                    "card_id": {"type": "string", "description": "Card ID to block"},
                    "reason": {"type": "string", "description": "Reason for blocking"},
                },
                "required": ["card_id", "reason"],
            },
        ),
        Tool(
            name="set_card_limit",
            description="Update the spending limit for a card.",
            inputSchema={
                "type": "object",
                "properties": {
                    "card_id": {"type": "string", "description": "Card ID"},
                    "new_limit": {"type": "number", "description": "New limit amount in USD"},
                },
                "required": ["card_id", "new_limit"],
            },
        ),
        Tool(
            name="get_card_details",
            description="Get full details of a card.",
            inputSchema={
                "type": "object",
                "properties": {"card_id": {"type": "string", "description": "Card ID"}},
                "required": ["card_id"],
            },
        ),
        Tool(
            name="get_rewards_balance",
            description="Check rewards points balance for a card.",
            inputSchema={
                "type": "object",
                "properties": {"card_id": {"type": "string", "description": "Card ID"}},
                "required": ["card_id"],
            },
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    if name == "issue_card":
        card_id = f"CARD-{uuid.uuid4().hex[:4].upper()}"
        last_four = str(uuid.uuid4().int)[:4]
        card = {
            "card_id": card_id,
            "account_id": arguments["account_id"],
            "card_type": arguments["card_type"],
            "card_number": f"****-****-****-{last_four}",
            "status": "active",
            "rewards_points": 0,
            "issued_at": datetime.utcnow().isoformat() + "Z",
        }
        if arguments["card_type"] == "credit":
            card["credit_limit"] = arguments.get("credit_limit", 5000.00)
            card["available_limit"] = card["credit_limit"]
        else:
            card["daily_limit"] = 5000.00
        CARDS[card_id] = card
        return [TextContent(type="text", text=json.dumps({"status": "issued", "card": card}))]

    elif name == "block_card":
        card = CARDS.get(arguments["card_id"])
        if not card:
            return [TextContent(type="text", text=json.dumps({"error": "Card not found"}))]
        card["status"] = "blocked"
        card["blocked_reason"] = arguments["reason"]
        card["blocked_at"] = datetime.utcnow().isoformat() + "Z"
        return [TextContent(type="text", text=json.dumps({"status": "blocked", "card": card}))]

    elif name == "set_card_limit":
        card = CARDS.get(arguments["card_id"])
        if not card:
            return [TextContent(type="text", text=json.dumps({"error": "Card not found"}))]
        if card["card_type"] == "credit":
            card["credit_limit"] = arguments["new_limit"]
        else:
            card["daily_limit"] = arguments["new_limit"]
        return [TextContent(type="text", text=json.dumps({"status": "limit_updated", "card": card}))]

    elif name == "get_card_details":
        card = CARDS.get(arguments["card_id"])
        if not card:
            return [TextContent(type="text", text=json.dumps({"error": "Card not found"}))]
        return [TextContent(type="text", text=json.dumps(card))]

    elif name == "get_rewards_balance":
        card = CARDS.get(arguments["card_id"])
        if not card:
            return [TextContent(type="text", text=json.dumps({"error": "Card not found"}))]
        return [TextContent(type="text", text=json.dumps({
            "card_id": card["card_id"],
            "rewards_points": card["rewards_points"],
            "estimated_value_usd": round(card["rewards_points"] * 0.01, 2),
        }))]

    return [TextContent(type="text", text=json.dumps({"error": f"Unknown tool: {name}"}))]


async def main():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
