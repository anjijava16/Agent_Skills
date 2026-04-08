"""MCP Server #8 — Insurance Engine.

Provides tools for policy quotes, claims management, and coverage.
"""

import json
import uuid
from datetime import datetime
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

server = Server("insurance-engine-mcp")

POLICIES: dict[str, dict] = {
    "POL-5001": {
        "policy_id": "POL-5001",
        "account_id": "ACC-1001",
        "type": "life",
        "coverage_amount": 500000.00,
        "premium_monthly": 120.00,
        "status": "active",
        "start_date": "2024-01-01",
        "end_date": "2034-01-01",
    },
    "POL-5002": {
        "policy_id": "POL-5002",
        "account_id": "ACC-1002",
        "type": "health",
        "coverage_amount": 100000.00,
        "premium_monthly": 85.00,
        "status": "active",
        "start_date": "2024-04-01",
        "end_date": "2025-04-01",
    },
}

CLAIMS: list[dict] = []


@server.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="get_policy_quote",
            description="Get an insurance premium quote.",
            inputSchema={
                "type": "object",
                "properties": {
                    "insurance_type": {"type": "string", "enum": ["life", "health", "auto", "home"], "description": "Insurance type"},
                    "coverage_amount": {"type": "number", "description": "Desired coverage in USD"},
                    "age": {"type": "integer", "description": "Applicant age"},
                },
                "required": ["insurance_type", "coverage_amount"],
            },
        ),
        Tool(
            name="create_policy",
            description="Create a new insurance policy.",
            inputSchema={
                "type": "object",
                "properties": {
                    "account_id": {"type": "string", "description": "Account ID"},
                    "insurance_type": {"type": "string", "enum": ["life", "health", "auto", "home"]},
                    "coverage_amount": {"type": "number", "description": "Coverage amount in USD"},
                    "term_years": {"type": "integer", "description": "Policy term in years"},
                },
                "required": ["account_id", "insurance_type", "coverage_amount", "term_years"],
            },
        ),
        Tool(
            name="file_claim",
            description="File an insurance claim.",
            inputSchema={
                "type": "object",
                "properties": {
                    "policy_id": {"type": "string", "description": "Policy ID"},
                    "claim_amount": {"type": "number", "description": "Claim amount in USD"},
                    "description": {"type": "string", "description": "Description of the claim"},
                },
                "required": ["policy_id", "claim_amount", "description"],
            },
        ),
        Tool(
            name="get_claim_status",
            description="Check the status of an insurance claim.",
            inputSchema={
                "type": "object",
                "properties": {"claim_id": {"type": "string", "description": "Claim ID"}},
                "required": ["claim_id"],
            },
        ),
        Tool(
            name="list_policies",
            description="List all insurance policies for an account.",
            inputSchema={
                "type": "object",
                "properties": {"account_id": {"type": "string", "description": "Account ID"}},
                "required": ["account_id"],
            },
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    if name == "get_policy_quote":
        rate_map = {"life": 0.0024, "health": 0.0085, "auto": 0.005, "home": 0.003}
        ins_type = arguments["insurance_type"]
        coverage = arguments["coverage_amount"]
        age_factor = 1.0 + (arguments.get("age", 30) - 25) * 0.01
        monthly = round(coverage * rate_map.get(ins_type, 0.004) * age_factor / 12, 2)
        return [TextContent(type="text", text=json.dumps({
            "insurance_type": ins_type,
            "coverage_amount": coverage,
            "estimated_monthly_premium": monthly,
            "estimated_annual_premium": round(monthly * 12, 2),
        }))]

    elif name == "create_policy":
        policy_id = f"POL-{uuid.uuid4().hex[:4].upper()}"
        rate_map = {"life": 0.0024, "health": 0.0085, "auto": 0.005, "home": 0.003}
        monthly = round(arguments["coverage_amount"] * rate_map.get(arguments["insurance_type"], 0.004) / 12, 2)
        policy = {
            "policy_id": policy_id,
            "account_id": arguments["account_id"],
            "type": arguments["insurance_type"],
            "coverage_amount": arguments["coverage_amount"],
            "premium_monthly": monthly,
            "status": "active",
            "start_date": datetime.utcnow().strftime("%Y-%m-%d"),
            "end_date": str(datetime.utcnow().year + arguments["term_years"]) + datetime.utcnow().strftime("-%m-%d"),
        }
        POLICIES[policy_id] = policy
        return [TextContent(type="text", text=json.dumps({"status": "created", "policy": policy}))]

    elif name == "file_claim":
        policy = POLICIES.get(arguments["policy_id"])
        if not policy:
            return [TextContent(type="text", text=json.dumps({"error": "Policy not found"}))]
        claim_id = f"CLM-{uuid.uuid4().hex[:4].upper()}"
        claim = {
            "claim_id": claim_id,
            "policy_id": arguments["policy_id"],
            "claim_amount": arguments["claim_amount"],
            "description": arguments["description"],
            "status": "under_review",
            "filed_at": datetime.utcnow().isoformat() + "Z",
        }
        CLAIMS.append(claim)
        return [TextContent(type="text", text=json.dumps({"status": "filed", "claim": claim}))]

    elif name == "get_claim_status":
        claim = next((c for c in CLAIMS if c["claim_id"] == arguments["claim_id"]), None)
        if not claim:
            return [TextContent(type="text", text=json.dumps({"error": "Claim not found"}))]
        return [TextContent(type="text", text=json.dumps(claim))]

    elif name == "list_policies":
        policies = [p for p in POLICIES.values() if p["account_id"] == arguments["account_id"]]
        return [TextContent(type="text", text=json.dumps({"account_id": arguments["account_id"], "policies": policies, "count": len(policies)}))]

    return [TextContent(type="text", text=json.dumps({"error": f"Unknown tool: {name}"}))]


async def main():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
