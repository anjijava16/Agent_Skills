"""MCP Server #3 — Loan Engine.

Provides tools for loan applications, EMI calculations, approvals, and schedules.
"""

import json
import uuid
import math
from datetime import datetime
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

server = Server("loan-engine-mcp")

LOANS: dict[str, dict] = {
    "LOAN-2001": {
        "loan_id": "LOAN-2001",
        "account_id": "ACC-1001",
        "loan_type": "home",
        "principal": 200000.00,
        "interest_rate": 6.5,
        "tenure_months": 240,
        "emi": 1491.15,
        "status": "active",
        "disbursed_at": "2024-02-01T00:00:00Z",
    },
    "LOAN-2002": {
        "loan_id": "LOAN-2002",
        "account_id": "ACC-1002",
        "loan_type": "personal",
        "principal": 15000.00,
        "interest_rate": 10.5,
        "tenure_months": 36,
        "emi": 487.68,
        "status": "active",
        "disbursed_at": "2024-05-10T00:00:00Z",
    },
}


def _calculate_emi(principal: float, annual_rate: float, tenure_months: int) -> float:
    monthly_rate = annual_rate / (12 * 100)
    if monthly_rate == 0:
        return principal / tenure_months
    emi = principal * monthly_rate * math.pow(1 + monthly_rate, tenure_months) / (
        math.pow(1 + monthly_rate, tenure_months) - 1
    )
    return round(emi, 2)


@server.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="apply_loan",
            description="Submit a new loan application.",
            inputSchema={
                "type": "object",
                "properties": {
                    "account_id": {"type": "string", "description": "Applicant account ID"},
                    "loan_type": {"type": "string", "enum": ["home", "personal", "auto", "education"], "description": "Type of loan"},
                    "principal": {"type": "number", "description": "Loan amount requested in USD"},
                    "tenure_months": {"type": "integer", "description": "Repayment period in months"},
                },
                "required": ["account_id", "loan_type", "principal", "tenure_months"],
            },
        ),
        Tool(
            name="get_loan_status",
            description="Check the status of a loan by loan ID.",
            inputSchema={
                "type": "object",
                "properties": {"loan_id": {"type": "string", "description": "The loan ID"}},
                "required": ["loan_id"],
            },
        ),
        Tool(
            name="calculate_emi",
            description="Calculate the monthly EMI for a loan.",
            inputSchema={
                "type": "object",
                "properties": {
                    "principal": {"type": "number", "description": "Loan principal in USD"},
                    "annual_rate": {"type": "number", "description": "Annual interest rate (e.g. 6.5 for 6.5%)"},
                    "tenure_months": {"type": "integer", "description": "Tenure in months"},
                },
                "required": ["principal", "annual_rate", "tenure_months"],
            },
        ),
        Tool(
            name="get_loan_schedule",
            description="Get the amortization schedule for a loan (first 12 months).",
            inputSchema={
                "type": "object",
                "properties": {"loan_id": {"type": "string", "description": "The loan ID"}},
                "required": ["loan_id"],
            },
        ),
        Tool(
            name="approve_loan",
            description="Approve a pending loan application.",
            inputSchema={
                "type": "object",
                "properties": {
                    "loan_id": {"type": "string", "description": "The loan ID to approve"},
                    "interest_rate": {"type": "number", "description": "Approved interest rate"},
                },
                "required": ["loan_id", "interest_rate"],
            },
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    if name == "apply_loan":
        loan_id = f"LOAN-{uuid.uuid4().hex[:4].upper()}"
        rate_map = {"home": 6.5, "personal": 10.5, "auto": 8.0, "education": 5.0}
        rate = rate_map.get(arguments["loan_type"], 9.0)
        emi = _calculate_emi(arguments["principal"], rate, arguments["tenure_months"])
        loan = {
            "loan_id": loan_id,
            "account_id": arguments["account_id"],
            "loan_type": arguments["loan_type"],
            "principal": arguments["principal"],
            "interest_rate": rate,
            "tenure_months": arguments["tenure_months"],
            "emi": emi,
            "status": "pending_approval",
            "applied_at": datetime.utcnow().isoformat() + "Z",
        }
        LOANS[loan_id] = loan
        return [TextContent(type="text", text=json.dumps({"status": "application_submitted", "loan": loan}))]

    elif name == "get_loan_status":
        loan = LOANS.get(arguments["loan_id"])
        if not loan:
            return [TextContent(type="text", text=json.dumps({"error": "Loan not found"}))]
        return [TextContent(type="text", text=json.dumps(loan))]

    elif name == "calculate_emi":
        emi = _calculate_emi(arguments["principal"], arguments["annual_rate"], arguments["tenure_months"])
        total_payment = emi * arguments["tenure_months"]
        total_interest = total_payment - arguments["principal"]
        return [TextContent(type="text", text=json.dumps({
            "emi": emi,
            "total_payment": round(total_payment, 2),
            "total_interest": round(total_interest, 2),
            "principal": arguments["principal"],
            "annual_rate": arguments["annual_rate"],
            "tenure_months": arguments["tenure_months"],
        }))]

    elif name == "get_loan_schedule":
        loan = LOANS.get(arguments["loan_id"])
        if not loan:
            return [TextContent(type="text", text=json.dumps({"error": "Loan not found"}))]
        schedule = []
        balance = loan["principal"]
        monthly_rate = loan["interest_rate"] / (12 * 100)
        for month in range(1, min(13, loan["tenure_months"] + 1)):
            interest = round(balance * monthly_rate, 2)
            principal_part = round(loan["emi"] - interest, 2)
            balance = round(balance - principal_part, 2)
            schedule.append({"month": month, "emi": loan["emi"], "interest": interest, "principal": principal_part, "balance": max(balance, 0)})
        return [TextContent(type="text", text=json.dumps({"loan_id": loan["loan_id"], "schedule": schedule}))]

    elif name == "approve_loan":
        loan = LOANS.get(arguments["loan_id"])
        if not loan:
            return [TextContent(type="text", text=json.dumps({"error": "Loan not found"}))]
        loan["status"] = "approved"
        loan["interest_rate"] = arguments["interest_rate"]
        loan["emi"] = _calculate_emi(loan["principal"], arguments["interest_rate"], loan["tenure_months"])
        return [TextContent(type="text", text=json.dumps({"status": "approved", "loan": loan}))]

    return [TextContent(type="text", text=json.dumps({"error": f"Unknown tool: {name}"}))]


async def main():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
