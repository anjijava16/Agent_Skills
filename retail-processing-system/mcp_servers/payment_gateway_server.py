"""FastMCP Server #5 — Payment Gateway (port 9005).

Tools for payment processing, refunds, transaction history, and verification.
"""

import asyncio
import logging
import os
import uuid
from datetime import datetime
from typing import Optional

from fastmcp import FastMCP

logger = logging.getLogger(__name__)
logging.basicConfig(format="[%(levelname)s]: %(message)s", level=logging.INFO)

mcp = FastMCP("Payment Gateway MCP Server 💳")

# ---------------------------------------------------------------------------
# In-memory transaction store
# ---------------------------------------------------------------------------

TRANSACTIONS = {
    "TXN-5001": {
        "transaction_id": "TXN-5001",
        "order_id": "ORD-2001",
        "customer_id": "CUST-100",
        "amount": 999.99,
        "currency": "USD",
        "method": "credit_card",
        "card_last4": "4242",
        "status": "completed",
        "created_at": "2025-01-10T10:30:00Z",
    },
    "TXN-5002": {
        "transaction_id": "TXN-5002",
        "order_id": "ORD-2002",
        "customer_id": "CUST-101",
        "amount": 159.98,
        "currency": "USD",
        "method": "debit_card",
        "card_last4": "1234",
        "status": "completed",
        "created_at": "2025-01-12T14:00:00Z",
    },
}


@mcp.tool()
def process_payment(
    order_id: str,
    customer_id: str,
    amount: float,
    method: str = "credit_card",
    currency: str = "USD",
) -> dict:
    """Process a payment for an order.

    Args:
        order_id: Associated order.
        customer_id: Paying customer.
        amount: Amount to charge.
        method: Payment method — 'credit_card', 'debit_card', 'digital_wallet'.
        currency: ISO currency code.

    Returns:
        Transaction confirmation with ID and status.
    """
    logger.info(f"--- 💳 process_payment ORD={order_id} ${amount} ---")
    if amount <= 0:
        return {"error": "Amount must be positive"}
    if method not in ("credit_card", "debit_card", "digital_wallet"):
        return {"error": f"Unsupported method: {method}"}
    txn_id = f"TXN-{uuid.uuid4().hex[:4].upper()}"
    txn = {
        "transaction_id": txn_id,
        "order_id": order_id,
        "customer_id": customer_id,
        "amount": amount,
        "currency": currency,
        "method": method,
        "card_last4": "****",
        "status": "completed",
        "created_at": datetime.utcnow().isoformat() + "Z",
    }
    TRANSACTIONS[txn_id] = txn
    return {"status": "payment_completed", "transaction": txn}


@mcp.tool()
def refund_payment(
    transaction_id: str,
    amount: Optional[float] = None,
    reason: str = "customer_request",
) -> dict:
    """Refund a previous payment (full or partial).

    Args:
        transaction_id: Original transaction to refund.
        amount: Partial refund amount (omit for full refund).
        reason: Reason for refund.

    Returns:
        Refund confirmation details.
    """
    logger.info(f"--- 🔄 refund_payment {transaction_id} ---")
    original = TRANSACTIONS.get(transaction_id)
    if not original:
        return {"error": f"Transaction {transaction_id} not found"}
    if original["status"] == "refunded":
        return {"error": "Transaction already refunded"}
    refund_amount = amount if amount else original["amount"]
    if refund_amount > original["amount"]:
        return {"error": "Refund exceeds original amount"}
    refund_id = f"REF-{uuid.uuid4().hex[:4].upper()}"
    if refund_amount == original["amount"]:
        original["status"] = "refunded"
    else:
        original["status"] = "partially_refunded"
    return {
        "refund_id": refund_id,
        "original_transaction": transaction_id,
        "refund_amount": refund_amount,
        "reason": reason,
        "status": "refund_completed",
    }


@mcp.tool()
def get_payment_status(transaction_id: str) -> dict:
    """Check the status of a payment transaction.

    Args:
        transaction_id: Transaction to look up.

    Returns:
        Transaction status details.
    """
    logger.info(f"--- 🔍 get_payment_status {transaction_id} ---")
    txn = TRANSACTIONS.get(transaction_id)
    if not txn:
        return {"error": f"Transaction {transaction_id} not found"}
    return {
        "transaction_id": txn["transaction_id"],
        "order_id": txn["order_id"],
        "amount": txn["amount"],
        "status": txn["status"],
        "method": txn["method"],
    }


@mcp.tool()
def list_transactions(
    customer_id: Optional[str] = None,
    order_id: Optional[str] = None,
    limit: int = 20,
) -> dict:
    """List payment transactions with optional filters.

    Args:
        customer_id: Filter by customer (optional).
        order_id: Filter by order (optional).
        limit: Max results.

    Returns:
        List of matching transactions.
    """
    logger.info(f"--- 📋 list_transactions cust={customer_id} ord={order_id} ---")
    results = []
    for txn in TRANSACTIONS.values():
        if customer_id and txn["customer_id"] != customer_id:
            continue
        if order_id and txn["order_id"] != order_id:
            continue
        results.append(txn)
        if len(results) >= limit:
            break
    return {"transactions": results, "count": len(results)}


@mcp.tool()
def verify_payment(transaction_id: str) -> dict:
    """Verify that a payment is authentic and completed.

    Args:
        transaction_id: Transaction to verify.

    Returns:
        Verification result with timestamp.
    """
    logger.info(f"--- ✅ verify_payment {transaction_id} ---")
    txn = TRANSACTIONS.get(transaction_id)
    if not txn:
        return {"verified": False, "reason": "Transaction not found"}
    is_valid = txn["status"] in ("completed", "partially_refunded")
    return {
        "transaction_id": transaction_id,
        "verified": is_valid,
        "status": txn["status"],
        "amount": txn["amount"],
        "verified_at": datetime.utcnow().isoformat() + "Z",
    }


if __name__ == "__main__":
    port = int(os.getenv("PAYMENT_MCP_PORT", "9005"))
    logger.info(f"💳 Payment Gateway MCP starting on port {port}")
    asyncio.run(mcp.run_async(transport="sse", host="0.0.0.0", port=port))
