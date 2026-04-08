"""MCP Server #5 — Fraud Engine.

Provides tools for transaction risk assessment, suspicious activity flagging, and alerts.
"""

import json
import uuid
from datetime import datetime
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

server = Server("fraud-engine-mcp")

FRAUD_ALERTS: list[dict] = [
    {
        "alert_id": "ALERT-001",
        "account_id": "ACC-1003",
        "txn_id": "TXN-FAKE-01",
        "risk_score": 0.92,
        "reason": "Unusual overseas transaction of $5,000",
        "status": "open",
        "created_at": "2024-06-10T03:00:00Z",
    },
]


@server.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="check_transaction_risk",
            description="Assess the fraud risk score for a proposed transaction.",
            inputSchema={
                "type": "object",
                "properties": {
                    "from_account": {"type": "string", "description": "Source account ID"},
                    "to_account": {"type": "string", "description": "Destination account or payee"},
                    "amount": {"type": "number", "description": "Transaction amount in USD"},
                    "transaction_type": {"type": "string", "description": "Type: transfer, payment, withdrawal"},
                },
                "required": ["from_account", "amount"],
            },
        ),
        Tool(
            name="flag_suspicious",
            description="Flag a transaction or account as suspicious.",
            inputSchema={
                "type": "object",
                "properties": {
                    "account_id": {"type": "string", "description": "Account ID"},
                    "txn_id": {"type": "string", "description": "Transaction ID (if applicable)"},
                    "reason": {"type": "string", "description": "Reason for flagging"},
                },
                "required": ["account_id", "reason"],
            },
        ),
        Tool(
            name="get_fraud_alerts",
            description="Get all fraud alerts, optionally filtered by account.",
            inputSchema={
                "type": "object",
                "properties": {
                    "account_id": {"type": "string", "description": "Filter by account ID"},
                    "status": {"type": "string", "enum": ["open", "investigating", "resolved"], "description": "Filter by alert status"},
                },
            },
        ),
        Tool(
            name="verify_transaction",
            description="Verify and clear a flagged transaction as legitimate.",
            inputSchema={
                "type": "object",
                "properties": {
                    "alert_id": {"type": "string", "description": "Alert ID to resolve"},
                    "verified_by": {"type": "string", "description": "Name of verifier"},
                },
                "required": ["alert_id"],
            },
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    if name == "check_transaction_risk":
        amount = arguments["amount"]
        # Simple risk scoring heuristic
        risk_score = 0.1
        risk_factors = []
        if amount > 10000:
            risk_score += 0.4
            risk_factors.append("high_value_transaction")
        if amount > 5000:
            risk_score += 0.2
            risk_factors.append("above_average_amount")
        if arguments.get("to_account", "").startswith("EXT"):
            risk_score += 0.2
            risk_factors.append("external_recipient")
        risk_level = "low" if risk_score < 0.3 else "medium" if risk_score < 0.6 else "high"
        return [TextContent(type="text", text=json.dumps({
            "risk_score": min(round(risk_score, 2), 1.0),
            "risk_level": risk_level,
            "risk_factors": risk_factors,
            "recommendation": "block" if risk_level == "high" else "review" if risk_level == "medium" else "allow",
        }))]

    elif name == "flag_suspicious":
        alert_id = f"ALERT-{uuid.uuid4().hex[:4].upper()}"
        alert = {
            "alert_id": alert_id,
            "account_id": arguments["account_id"],
            "txn_id": arguments.get("txn_id", "N/A"),
            "risk_score": 0.85,
            "reason": arguments["reason"],
            "status": "open",
            "created_at": datetime.utcnow().isoformat() + "Z",
        }
        FRAUD_ALERTS.append(alert)
        return [TextContent(type="text", text=json.dumps({"status": "flagged", "alert": alert}))]

    elif name == "get_fraud_alerts":
        alerts = FRAUD_ALERTS[:]
        if arguments.get("account_id"):
            alerts = [a for a in alerts if a["account_id"] == arguments["account_id"]]
        if arguments.get("status"):
            alerts = [a for a in alerts if a["status"] == arguments["status"]]
        return [TextContent(type="text", text=json.dumps({"alerts": alerts, "count": len(alerts)}))]

    elif name == "verify_transaction":
        alert = next((a for a in FRAUD_ALERTS if a["alert_id"] == arguments["alert_id"]), None)
        if not alert:
            return [TextContent(type="text", text=json.dumps({"error": "Alert not found"}))]
        alert["status"] = "resolved"
        alert["verified_by"] = arguments.get("verified_by", "system")
        alert["resolved_at"] = datetime.utcnow().isoformat() + "Z"
        return [TextContent(type="text", text=json.dumps({"status": "verified", "alert": alert}))]

    return [TextContent(type="text", text=json.dumps({"error": f"Unknown tool: {name}"}))]


async def main():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
