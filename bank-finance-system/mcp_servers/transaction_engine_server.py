"""MCP Server #2 — Transaction Engine.

Provides tools for transfers, payments, deposits, withdrawals, and history.
"""

import json
import uuid
from datetime import datetime
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

server = Server("transaction-engine-mcp")

# --- In-Memory Data Store ---
TRANSACTIONS: list[dict] = [
    {
        "txn_id": "TXN-0001",
        "from_account": "ACC-1001",
        "to_account": "ACC-1002",
        "amount": 500.00,
        "currency": "USD",
        "type": "transfer",
        "status": "completed",
        "timestamp": "2024-06-01T10:30:00Z",
        "description": "Monthly rent payment",
    },
    {
        "txn_id": "TXN-0002",
        "from_account": "ACC-1002",
        "to_account": "EXTERNAL",
        "amount": 150.00,
        "currency": "USD",
        "type": "payment",
        "status": "completed",
        "timestamp": "2024-06-05T14:00:00Z",
        "description": "Utility bill payment",
    },
]


@server.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="process_transfer",
            description="Transfer money between two accounts.",
            inputSchema={
                "type": "object",
                "properties": {
                    "from_account": {"type": "string", "description": "Source account ID"},
                    "to_account": {"type": "string", "description": "Destination account ID"},
                    "amount": {"type": "number", "description": "Amount to transfer in USD"},
                    "description": {"type": "string", "description": "Transfer description"},
                },
                "required": ["from_account", "to_account", "amount"],
            },
        ),
        Tool(
            name="process_payment",
            description="Process an outbound payment to a payee.",
            inputSchema={
                "type": "object",
                "properties": {
                    "from_account": {"type": "string", "description": "Source account ID"},
                    "payee": {"type": "string", "description": "Payee name or reference"},
                    "amount": {"type": "number", "description": "Payment amount in USD"},
                    "description": {"type": "string", "description": "Payment description"},
                },
                "required": ["from_account", "payee", "amount"],
            },
        ),
        Tool(
            name="get_transaction_history",
            description="Get transaction history for an account.",
            inputSchema={
                "type": "object",
                "properties": {
                    "account_id": {"type": "string", "description": "Account ID to query"},
                    "limit": {"type": "integer", "description": "Max number of transactions to return"},
                },
                "required": ["account_id"],
            },
        ),
        Tool(
            name="get_statement",
            description="Generate a mini account statement with recent transactions and balance summary.",
            inputSchema={
                "type": "object",
                "properties": {
                    "account_id": {"type": "string", "description": "Account ID"},
                    "period_days": {"type": "integer", "description": "Number of days to include (default: 30)"},
                },
                "required": ["account_id"],
            },
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    if name == "process_transfer":
        txn_id = f"TXN-{uuid.uuid4().hex[:6].upper()}"
        txn = {
            "txn_id": txn_id,
            "from_account": arguments["from_account"],
            "to_account": arguments["to_account"],
            "amount": arguments["amount"],
            "currency": "USD",
            "type": "transfer",
            "status": "completed",
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "description": arguments.get("description", "Fund transfer"),
        }
        TRANSACTIONS.append(txn)
        return [TextContent(type="text", text=json.dumps({"status": "success", "transaction": txn}))]

    elif name == "process_payment":
        txn_id = f"TXN-{uuid.uuid4().hex[:6].upper()}"
        txn = {
            "txn_id": txn_id,
            "from_account": arguments["from_account"],
            "to_account": arguments["payee"],
            "amount": arguments["amount"],
            "currency": "USD",
            "type": "payment",
            "status": "completed",
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "description": arguments.get("description", f"Payment to {arguments['payee']}"),
        }
        TRANSACTIONS.append(txn)
        return [TextContent(type="text", text=json.dumps({"status": "success", "transaction": txn}))]

    elif name == "get_transaction_history":
        account_id = arguments["account_id"]
        limit = arguments.get("limit", 20)
        history = [
            t for t in TRANSACTIONS
            if t["from_account"] == account_id or t["to_account"] == account_id
        ][:limit]
        return [TextContent(type="text", text=json.dumps({"account_id": account_id, "transactions": history, "count": len(history)}))]

    elif name == "get_statement":
        account_id = arguments["account_id"]
        history = [
            t for t in TRANSACTIONS
            if t["from_account"] == account_id or t["to_account"] == account_id
        ]
        total_debit = sum(t["amount"] for t in history if t["from_account"] == account_id)
        total_credit = sum(t["amount"] for t in history if t["to_account"] == account_id)
        return [TextContent(type="text", text=json.dumps({
            "account_id": account_id,
            "period_days": arguments.get("period_days", 30),
            "total_debit": total_debit,
            "total_credit": total_credit,
            "net_flow": total_credit - total_debit,
            "transaction_count": len(history),
            "transactions": history,
        }))]

    return [TextContent(type="text", text=json.dumps({"error": f"Unknown tool: {name}"}))]


async def main():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
