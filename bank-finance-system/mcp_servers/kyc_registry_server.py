"""MCP Server #6 — KYC Registry.

Provides tools for identity verification, document checks, and AML screening.
"""

import json
import uuid
from datetime import datetime
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

server = Server("kyc-registry-mcp")

KYC_RECORDS: dict[str, dict] = {
    "ACC-1001": {
        "account_id": "ACC-1001",
        "kyc_status": "verified",
        "id_type": "passport",
        "id_number": "P****5678",
        "verified_at": "2024-01-15T11:00:00Z",
        "aml_clear": True,
        "risk_category": "low",
    },
    "ACC-1002": {
        "account_id": "ACC-1002",
        "kyc_status": "verified",
        "id_type": "drivers_license",
        "id_number": "DL****2345",
        "verified_at": "2024-03-20T15:00:00Z",
        "aml_clear": True,
        "risk_category": "low",
    },
    "ACC-1003": {
        "account_id": "ACC-1003",
        "kyc_status": "pending",
        "id_type": "national_id",
        "id_number": "NI****9012",
        "aml_clear": False,
        "risk_category": "medium",
    },
}


@server.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="verify_identity",
            description="Verify a customer's identity using provided documents.",
            inputSchema={
                "type": "object",
                "properties": {
                    "account_id": {"type": "string", "description": "Account ID"},
                    "id_type": {"type": "string", "enum": ["passport", "drivers_license", "national_id"], "description": "Type of ID document"},
                    "id_number": {"type": "string", "description": "ID document number"},
                },
                "required": ["account_id", "id_type", "id_number"],
            },
        ),
        Tool(
            name="check_documents",
            description="Check if required KYC documents have been submitted.",
            inputSchema={
                "type": "object",
                "properties": {"account_id": {"type": "string", "description": "Account ID"}},
                "required": ["account_id"],
            },
        ),
        Tool(
            name="get_kyc_status",
            description="Get the current KYC verification status for an account.",
            inputSchema={
                "type": "object",
                "properties": {"account_id": {"type": "string", "description": "Account ID"}},
                "required": ["account_id"],
            },
        ),
        Tool(
            name="run_aml_check",
            description="Run an Anti-Money Laundering check on an account.",
            inputSchema={
                "type": "object",
                "properties": {
                    "account_id": {"type": "string", "description": "Account ID"},
                    "transaction_amount": {"type": "number", "description": "Amount to check against AML thresholds"},
                },
                "required": ["account_id"],
            },
        ),
        Tool(
            name="submit_kyc",
            description="Submit KYC documents for verification.",
            inputSchema={
                "type": "object",
                "properties": {
                    "account_id": {"type": "string", "description": "Account ID"},
                    "id_type": {"type": "string", "enum": ["passport", "drivers_license", "national_id"], "description": "Document type"},
                    "id_number": {"type": "string", "description": "Document number"},
                    "full_name": {"type": "string", "description": "Full legal name"},
                    "date_of_birth": {"type": "string", "description": "Date of birth (YYYY-MM-DD)"},
                },
                "required": ["account_id", "id_type", "id_number", "full_name"],
            },
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    if name == "verify_identity":
        record = KYC_RECORDS.get(arguments["account_id"])
        if record and record["kyc_status"] == "verified":
            return [TextContent(type="text", text=json.dumps({"status": "already_verified", "record": record}))]
        # Simulate verification
        masked_id = arguments["id_number"][:2] + "****" + arguments["id_number"][-4:]
        record = {
            "account_id": arguments["account_id"],
            "kyc_status": "verified",
            "id_type": arguments["id_type"],
            "id_number": masked_id,
            "verified_at": datetime.utcnow().isoformat() + "Z",
            "aml_clear": True,
            "risk_category": "low",
        }
        KYC_RECORDS[arguments["account_id"]] = record
        return [TextContent(type="text", text=json.dumps({"status": "verified", "record": record}))]

    elif name == "check_documents":
        record = KYC_RECORDS.get(arguments["account_id"])
        if not record:
            return [TextContent(type="text", text=json.dumps({"status": "no_documents", "documents_required": ["id_proof", "address_proof", "photo"]}))]
        return [TextContent(type="text", text=json.dumps({
            "account_id": arguments["account_id"],
            "documents_submitted": True,
            "id_type": record["id_type"],
            "kyc_status": record["kyc_status"],
        }))]

    elif name == "get_kyc_status":
        record = KYC_RECORDS.get(arguments["account_id"])
        if not record:
            return [TextContent(type="text", text=json.dumps({"account_id": arguments["account_id"], "kyc_status": "not_started"}))]
        return [TextContent(type="text", text=json.dumps(record))]

    elif name == "run_aml_check":
        record = KYC_RECORDS.get(arguments["account_id"])
        amount = arguments.get("transaction_amount", 0)
        aml_clear = amount < 50000
        risk = "high" if amount > 50000 else "medium" if amount > 10000 else "low"
        return [TextContent(type="text", text=json.dumps({
            "account_id": arguments["account_id"],
            "aml_clear": aml_clear,
            "risk_level": risk,
            "checked_amount": amount,
            "threshold": 50000,
            "recommendation": "approve" if aml_clear else "manual_review",
        }))]

    elif name == "submit_kyc":
        masked_id = arguments["id_number"][:2] + "****" + arguments["id_number"][-4:]
        record = {
            "account_id": arguments["account_id"],
            "kyc_status": "under_review",
            "id_type": arguments["id_type"],
            "id_number": masked_id,
            "full_name": arguments["full_name"],
            "aml_clear": False,
            "risk_category": "pending",
            "submitted_at": datetime.utcnow().isoformat() + "Z",
        }
        KYC_RECORDS[arguments["account_id"]] = record
        return [TextContent(type="text", text=json.dumps({"status": "submitted", "record": record}))]

    return [TextContent(type="text", text=json.dumps({"error": f"Unknown tool: {name}"}))]


async def main():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
