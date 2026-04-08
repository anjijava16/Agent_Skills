"""MCP Server #1 — Account Database.

Provides tools for account CRUD and balance inquiries.
Uses in-memory simulated data.
"""

import json
import uuid
from datetime import datetime
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

server = Server("account-db-mcp")

# --- In-Memory Data Store ---
ACCOUNTS: dict[str, dict] = {
    "ACC-1001": {
        "account_id": "ACC-1001",
        "customer_name": "Alice Johnson",
        "account_type": "savings",
        "balance": 25000.00,
        "currency": "USD",
        "status": "active",
        "created_at": "2024-01-15T10:00:00Z",
    },
    "ACC-1002": {
        "account_id": "ACC-1002",
        "customer_name": "Bob Smith",
        "account_type": "checking",
        "balance": 8500.50,
        "currency": "USD",
        "status": "active",
        "created_at": "2024-03-20T14:30:00Z",
    },
    "ACC-1003": {
        "account_id": "ACC-1003",
        "customer_name": "Carol Williams",
        "account_type": "savings",
        "balance": 120000.00,
        "currency": "USD",
        "status": "active",
        "created_at": "2023-11-01T09:00:00Z",
    },
}


@server.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="get_account",
            description="Retrieve account details by account ID.",
            inputSchema={
                "type": "object",
                "properties": {
                    "account_id": {"type": "string", "description": "The account ID (e.g. ACC-1001)"}
                },
                "required": ["account_id"],
            },
        ),
        Tool(
            name="create_account",
            description="Create a new bank account for a customer.",
            inputSchema={
                "type": "object",
                "properties": {
                    "customer_name": {"type": "string", "description": "Full name of the customer"},
                    "account_type": {
                        "type": "string",
                        "enum": ["savings", "checking", "business"],
                        "description": "Type of account",
                    },
                    "initial_deposit": {
                        "type": "number",
                        "description": "Initial deposit amount in USD",
                    },
                },
                "required": ["customer_name", "account_type", "initial_deposit"],
            },
        ),
        Tool(
            name="update_account",
            description="Update account details (status or account type).",
            inputSchema={
                "type": "object",
                "properties": {
                    "account_id": {"type": "string", "description": "The account ID"},
                    "status": {
                        "type": "string",
                        "enum": ["active", "frozen", "closed"],
                        "description": "New account status",
                    },
                    "account_type": {
                        "type": "string",
                        "enum": ["savings", "checking", "business"],
                        "description": "New account type",
                    },
                },
                "required": ["account_id"],
            },
        ),
        Tool(
            name="get_balance",
            description="Get the current balance for an account.",
            inputSchema={
                "type": "object",
                "properties": {
                    "account_id": {"type": "string", "description": "The account ID"}
                },
                "required": ["account_id"],
            },
        ),
        Tool(
            name="list_accounts",
            description="List all accounts, optionally filtered by customer name or status.",
            inputSchema={
                "type": "object",
                "properties": {
                    "customer_name": {
                        "type": "string",
                        "description": "Filter by customer name (partial match)",
                    },
                    "status": {
                        "type": "string",
                        "enum": ["active", "frozen", "closed"],
                        "description": "Filter by account status",
                    },
                },
            },
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    if name == "get_account":
        account_id = arguments["account_id"]
        account = ACCOUNTS.get(account_id)
        if not account:
            return [TextContent(type="text", text=json.dumps({"error": f"Account {account_id} not found"}))]
        return [TextContent(type="text", text=json.dumps(account))]

    elif name == "create_account":
        account_id = f"ACC-{uuid.uuid4().hex[:4].upper()}"
        account = {
            "account_id": account_id,
            "customer_name": arguments["customer_name"],
            "account_type": arguments["account_type"],
            "balance": arguments["initial_deposit"],
            "currency": "USD",
            "status": "active",
            "created_at": datetime.utcnow().isoformat() + "Z",
        }
        ACCOUNTS[account_id] = account
        return [TextContent(type="text", text=json.dumps({"status": "created", "account": account}))]

    elif name == "update_account":
        account_id = arguments["account_id"]
        account = ACCOUNTS.get(account_id)
        if not account:
            return [TextContent(type="text", text=json.dumps({"error": f"Account {account_id} not found"}))]
        if "status" in arguments:
            account["status"] = arguments["status"]
        if "account_type" in arguments:
            account["account_type"] = arguments["account_type"]
        return [TextContent(type="text", text=json.dumps({"status": "updated", "account": account}))]

    elif name == "get_balance":
        account_id = arguments["account_id"]
        account = ACCOUNTS.get(account_id)
        if not account:
            return [TextContent(type="text", text=json.dumps({"error": f"Account {account_id} not found"}))]
        return [TextContent(
            type="text",
            text=json.dumps({
                "account_id": account_id,
                "balance": account["balance"],
                "currency": account["currency"],
            }),
        )]

    elif name == "list_accounts":
        results = list(ACCOUNTS.values())
        if "customer_name" in arguments and arguments["customer_name"]:
            query = arguments["customer_name"].lower()
            results = [a for a in results if query in a["customer_name"].lower()]
        if "status" in arguments and arguments["status"]:
            results = [a for a in results if a["status"] == arguments["status"]]
        return [TextContent(type="text", text=json.dumps({"accounts": results, "count": len(results)}))]

    return [TextContent(type="text", text=json.dumps({"error": f"Unknown tool: {name}"}))]


async def main():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream)


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
