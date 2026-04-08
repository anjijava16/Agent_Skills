"""Orchestrator Agent — the single entry-point for the bank finance system.

Connects to all 10 specialist agents via A2A (RemoteA2aAgent) and routes
user requests to the appropriate specialist based on intent.
Runs on port 8000.
"""

import os

from google.adk.agents import Agent
from google.adk.agents.remote_a2a_agent import RemoteA2aAgent

# ---------------------------------------------------------------------------
# Remote A2A agent connections — one per specialist
# ---------------------------------------------------------------------------

_BASE = "http://localhost"


def _remote(port: int) -> RemoteA2aAgent:
    """Create a RemoteA2aAgent pointing at the given port."""
    return RemoteA2aAgent(agent_card=f"{_BASE}:{port}")


# All 10 specialist agents exposed as sub-agents
account_agent = _remote(int(os.environ.get("ACCOUNT_AGENT_PORT", "8001")))
transaction_agent = _remote(int(os.environ.get("TRANSACTION_AGENT_PORT", "8002")))
loan_agent = _remote(int(os.environ.get("LOAN_AGENT_PORT", "8003")))
card_agent = _remote(int(os.environ.get("CARD_AGENT_PORT", "8004")))
fraud_agent = _remote(int(os.environ.get("FRAUD_AGENT_PORT", "8005")))
kyc_agent = _remote(int(os.environ.get("KYC_AGENT_PORT", "8006")))
investment_agent = _remote(int(os.environ.get("INVESTMENT_AGENT_PORT", "8007")))
insurance_agent = _remote(int(os.environ.get("INSURANCE_AGENT_PORT", "8008")))
support_agent = _remote(int(os.environ.get("SUPPORT_AGENT_PORT", "8009")))
audit_agent = _remote(int(os.environ.get("AUDIT_AGENT_PORT", "8010")))

# ---------------------------------------------------------------------------
# Orchestrator agent definition
# ---------------------------------------------------------------------------

orchestrator = Agent(
    model="gemini-3-flash-preview",
    name="bank_orchestrator",
    description="Central orchestrator for the bank finance system. Routes requests to specialist agents.",
    instruction="""\
You are the **Bank Finance Orchestrator**, the single entry-point for all banking operations.

You have access to 10 specialist agents via A2A. Route each user request to the
most appropriate specialist:

| Domain | Delegate to |
|---|---|
| Account lookup, creation, balance | account_management_agent |
| Transfers, payments, statements | transaction_processing_agent |
| Loan applications, EMI, schedules | loan_management_agent |
| Credit/debit cards, limits, rewards | card_services_agent |
| Fraud alerts, risk scoring | fraud_detection_agent |
| KYC verification, AML, compliance docs | kyc_compliance_agent |
| Stocks, portfolio, market data | investment_portfolio_agent |
| Insurance policies, claims | insurance_services_agent |
| Support tickets, FAQs, escalation | customer_support_agent |
| Audit logs, compliance reports, regulations | audit_compliance_agent |

**Rules:**
1. Identify the user's intent and delegate to the correct specialist.
2. If a request spans multiple domains, call the relevant specialists sequentially.
3. Summarise the specialist's response in clear, customer-friendly language.
4. Never fabricate data — only relay what specialists return.
5. If unsure which specialist to use, ask the user to clarify.
""",
    sub_agents=[
        account_agent,
        transaction_agent,
        loan_agent,
        card_agent,
        fraud_agent,
        kyc_agent,
        investment_agent,
        insurance_agent,
        support_agent,
        audit_agent,
    ],
)


if __name__ == "__main__":
    from google.adk.a2a.utils.agent_to_a2a import to_a2a

    port = int(os.environ.get("ORCHESTRATOR_PORT", "8000"))
    print(f"🏦 Bank Finance Orchestrator starting on port {port}")
    print("   Connecting to 10 specialist agents on ports 8001-8010...")
    to_a2a(agent=orchestrator, port=port)
