"""MCP Server #10 — Audit Ledger.

Provides tools for audit trails, regulatory reports, and compliance checks.
"""

import json
import uuid
from datetime import datetime
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

server = Server("audit-ledger-mcp")

AUDIT_LOG: list[dict] = [
    {
        "event_id": "AUD-0001",
        "event_type": "account_created",
        "entity_id": "ACC-1001",
        "actor": "system",
        "details": "Account ACC-1001 created for Alice Johnson",
        "timestamp": "2024-01-15T10:00:00Z",
    },
    {
        "event_id": "AUD-0002",
        "event_type": "transaction",
        "entity_id": "TXN-0001",
        "actor": "ACC-1001",
        "details": "Transfer of $500 from ACC-1001 to ACC-1002",
        "timestamp": "2024-06-01T10:30:00Z",
    },
    {
        "event_id": "AUD-0003",
        "event_type": "kyc_verified",
        "entity_id": "ACC-1001",
        "actor": "compliance_team",
        "details": "KYC verification completed for ACC-1001",
        "timestamp": "2024-01-15T11:00:00Z",
    },
]

REGULATIONS = [
    {"code": "BSA", "name": "Bank Secrecy Act", "description": "Requires reporting of suspicious activity over $10,000"},
    {"code": "GDPR", "name": "General Data Protection Regulation", "description": "Customer data privacy and right to erasure"},
    {"code": "PCI-DSS", "name": "Payment Card Industry Data Security Standard", "description": "Card data handling and storage requirements"},
    {"code": "SOX", "name": "Sarbanes-Oxley Act", "description": "Financial reporting and internal controls"},
    {"code": "AML", "name": "Anti-Money Laundering", "description": "Transaction monitoring and suspicious activity reporting"},
]


@server.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="log_audit_event",
            description="Log a new event to the audit trail.",
            inputSchema={
                "type": "object",
                "properties": {
                    "event_type": {"type": "string", "description": "Type of event (e.g. transaction, account_created, login, policy_change)"},
                    "entity_id": {"type": "string", "description": "ID of the entity involved"},
                    "actor": {"type": "string", "description": "Who performed the action"},
                    "details": {"type": "string", "description": "Description of the event"},
                },
                "required": ["event_type", "entity_id", "actor", "details"],
            },
        ),
        Tool(
            name="get_audit_trail",
            description="Retrieve audit trail entries, optionally filtered.",
            inputSchema={
                "type": "object",
                "properties": {
                    "entity_id": {"type": "string", "description": "Filter by entity ID"},
                    "event_type": {"type": "string", "description": "Filter by event type"},
                    "limit": {"type": "integer", "description": "Max entries to return"},
                },
            },
        ),
        Tool(
            name="generate_report",
            description="Generate a compliance or audit summary report.",
            inputSchema={
                "type": "object",
                "properties": {
                    "report_type": {"type": "string", "enum": ["audit_summary", "transaction_report", "compliance_status"], "description": "Type of report"},
                    "period_days": {"type": "integer", "description": "Reporting period in days"},
                },
                "required": ["report_type"],
            },
        ),
        Tool(
            name="check_compliance",
            description="Check if an action complies with banking regulations.",
            inputSchema={
                "type": "object",
                "properties": {
                    "action_type": {"type": "string", "description": "Type of action to check"},
                    "amount": {"type": "number", "description": "Transaction amount if applicable"},
                    "details": {"type": "string", "description": "Additional context"},
                },
                "required": ["action_type"],
            },
        ),
        Tool(
            name="get_regulations",
            description="List applicable banking regulations and compliance requirements.",
            inputSchema={
                "type": "object",
                "properties": {
                    "category": {"type": "string", "description": "Filter by regulation category"},
                },
            },
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    if name == "log_audit_event":
        event_id = f"AUD-{uuid.uuid4().hex[:4].upper()}"
        event = {
            "event_id": event_id,
            "event_type": arguments["event_type"],
            "entity_id": arguments["entity_id"],
            "actor": arguments["actor"],
            "details": arguments["details"],
            "timestamp": datetime.utcnow().isoformat() + "Z",
        }
        AUDIT_LOG.append(event)
        return [TextContent(type="text", text=json.dumps({"status": "logged", "event": event}))]

    elif name == "get_audit_trail":
        results = AUDIT_LOG[:]
        if arguments.get("entity_id"):
            results = [e for e in results if e["entity_id"] == arguments["entity_id"]]
        if arguments.get("event_type"):
            results = [e for e in results if e["event_type"] == arguments["event_type"]]
        limit = arguments.get("limit", 50)
        results = results[-limit:]
        return [TextContent(type="text", text=json.dumps({"entries": results, "count": len(results)}))]

    elif name == "generate_report":
        report_type = arguments["report_type"]
        period = arguments.get("period_days", 30)
        report = {
            "report_type": report_type,
            "period_days": period,
            "generated_at": datetime.utcnow().isoformat() + "Z",
            "total_audit_entries": len(AUDIT_LOG),
        }
        if report_type == "audit_summary":
            types_count = {}
            for e in AUDIT_LOG:
                types_count[e["event_type"]] = types_count.get(e["event_type"], 0) + 1
            report["event_type_breakdown"] = types_count
        elif report_type == "transaction_report":
            txn_events = [e for e in AUDIT_LOG if e["event_type"] == "transaction"]
            report["transaction_count"] = len(txn_events)
            report["transactions"] = txn_events
        elif report_type == "compliance_status":
            report["regulations_checked"] = len(REGULATIONS)
            report["overall_status"] = "compliant"
            report["findings"] = []
        return [TextContent(type="text", text=json.dumps(report))]

    elif name == "check_compliance":
        issues = []
        amount = arguments.get("amount", 0)
        if amount > 10000:
            issues.append({"regulation": "BSA", "issue": "Transaction exceeds $10,000 — CTR filing required"})
        if arguments["action_type"] in ("data_export", "data_deletion"):
            issues.append({"regulation": "GDPR", "issue": "Data action requires privacy officer approval"})
        compliant = len(issues) == 0
        return [TextContent(type="text", text=json.dumps({
            "action_type": arguments["action_type"],
            "amount": amount,
            "compliant": compliant,
            "issues": issues,
            "recommendation": "proceed" if compliant else "requires_review",
        }))]

    elif name == "get_regulations":
        regs = REGULATIONS[:]
        if arguments.get("category"):
            regs = [r for r in regs if arguments["category"].lower() in r["name"].lower() or arguments["category"].lower() in r["code"].lower()]
        return [TextContent(type="text", text=json.dumps({"regulations": regs, "count": len(regs)}))]

    return [TextContent(type="text", text=json.dumps({"error": f"Unknown tool: {name}"}))]


async def main():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
