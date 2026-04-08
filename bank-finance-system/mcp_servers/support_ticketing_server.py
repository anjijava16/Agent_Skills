"""MCP Server #9 — Support Ticketing.

Provides tools for customer support tickets, FAQs, and escalation.
"""

import json
import uuid
from datetime import datetime
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

server = Server("support-ticketing-mcp")

TICKETS: dict[str, dict] = {
    "TKT-7001": {
        "ticket_id": "TKT-7001",
        "account_id": "ACC-1002",
        "subject": "Unable to access online banking",
        "description": "Getting error 403 when trying to login since yesterday.",
        "priority": "high",
        "status": "open",
        "created_at": "2024-06-12T09:00:00Z",
    },
}

FAQ_DB = [
    {"id": "FAQ-01", "question": "How do I reset my password?", "answer": "Go to the login page, click 'Forgot Password', and follow the email instructions."},
    {"id": "FAQ-02", "question": "What are the wire transfer fees?", "answer": "Domestic wire: $25, International wire: $45. Premium accounts get free domestic wires."},
    {"id": "FAQ-03", "question": "How do I order a new checkbook?", "answer": "Log into online banking → Services → Order Checkbook. Delivery takes 7-10 business days."},
    {"id": "FAQ-04", "question": "What is the daily ATM withdrawal limit?", "answer": "Standard: $500/day, Gold: $1,000/day, Platinum: $2,500/day."},
    {"id": "FAQ-05", "question": "How do I dispute a transaction?", "answer": "Call our fraud hotline or submit a dispute through online banking within 60 days of the transaction."},
]


@server.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="create_ticket",
            description="Create a new customer support ticket.",
            inputSchema={
                "type": "object",
                "properties": {
                    "account_id": {"type": "string", "description": "Customer account ID"},
                    "subject": {"type": "string", "description": "Ticket subject"},
                    "description": {"type": "string", "description": "Detailed description of the issue"},
                    "priority": {"type": "string", "enum": ["low", "medium", "high", "critical"], "description": "Priority level"},
                },
                "required": ["account_id", "subject", "description"],
            },
        ),
        Tool(
            name="get_ticket_status",
            description="Get the current status of a support ticket.",
            inputSchema={
                "type": "object",
                "properties": {"ticket_id": {"type": "string", "description": "Ticket ID"}},
                "required": ["ticket_id"],
            },
        ),
        Tool(
            name="update_ticket",
            description="Update a support ticket's status or add a note.",
            inputSchema={
                "type": "object",
                "properties": {
                    "ticket_id": {"type": "string", "description": "Ticket ID"},
                    "status": {"type": "string", "enum": ["open", "in_progress", "waiting_customer", "resolved", "closed"]},
                    "note": {"type": "string", "description": "Additional note to add"},
                },
                "required": ["ticket_id"],
            },
        ),
        Tool(
            name="search_faq",
            description="Search the FAQ knowledge base for answers.",
            inputSchema={
                "type": "object",
                "properties": {"query": {"type": "string", "description": "Search query"}},
                "required": ["query"],
            },
        ),
        Tool(
            name="escalate_ticket",
            description="Escalate a ticket to a senior support agent or manager.",
            inputSchema={
                "type": "object",
                "properties": {
                    "ticket_id": {"type": "string", "description": "Ticket ID to escalate"},
                    "reason": {"type": "string", "description": "Reason for escalation"},
                },
                "required": ["ticket_id", "reason"],
            },
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    if name == "create_ticket":
        ticket_id = f"TKT-{uuid.uuid4().hex[:4].upper()}"
        ticket = {
            "ticket_id": ticket_id,
            "account_id": arguments["account_id"],
            "subject": arguments["subject"],
            "description": arguments["description"],
            "priority": arguments.get("priority", "medium"),
            "status": "open",
            "created_at": datetime.utcnow().isoformat() + "Z",
        }
        TICKETS[ticket_id] = ticket
        return [TextContent(type="text", text=json.dumps({"status": "created", "ticket": ticket}))]

    elif name == "get_ticket_status":
        ticket = TICKETS.get(arguments["ticket_id"])
        if not ticket:
            return [TextContent(type="text", text=json.dumps({"error": "Ticket not found"}))]
        return [TextContent(type="text", text=json.dumps(ticket))]

    elif name == "update_ticket":
        ticket = TICKETS.get(arguments["ticket_id"])
        if not ticket:
            return [TextContent(type="text", text=json.dumps({"error": "Ticket not found"}))]
        if "status" in arguments:
            ticket["status"] = arguments["status"]
        if "note" in arguments:
            ticket.setdefault("notes", []).append({
                "note": arguments["note"],
                "added_at": datetime.utcnow().isoformat() + "Z",
            })
        return [TextContent(type="text", text=json.dumps({"status": "updated", "ticket": ticket}))]

    elif name == "search_faq":
        query = arguments["query"].lower()
        results = [
            faq for faq in FAQ_DB
            if query in faq["question"].lower() or query in faq["answer"].lower()
        ]
        if not results:
            # Broad match — return all FAQs with partial keyword match
            words = query.split()
            results = [
                faq for faq in FAQ_DB
                if any(w in faq["question"].lower() or w in faq["answer"].lower() for w in words)
            ]
        return [TextContent(type="text", text=json.dumps({"query": arguments["query"], "results": results, "count": len(results)}))]

    elif name == "escalate_ticket":
        ticket = TICKETS.get(arguments["ticket_id"])
        if not ticket:
            return [TextContent(type="text", text=json.dumps({"error": "Ticket not found"}))]
        ticket["status"] = "escalated"
        ticket["escalation_reason"] = arguments["reason"]
        ticket["escalated_at"] = datetime.utcnow().isoformat() + "Z"
        return [TextContent(type="text", text=json.dumps({"status": "escalated", "ticket": ticket}))]

    return [TextContent(type="text", text=json.dumps({"error": f"Unknown tool: {name}"}))]


async def main():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
