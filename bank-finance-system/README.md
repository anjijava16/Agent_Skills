# Bank Finance Multi-Agent System

A multi-agent banking system built with **Google ADK (Agent Development Kit)**, featuring 10 specialist agents, 10 MCP tool servers, A2A inter-agent communication, and a central orchestrator.

## Architecture

```
                    ┌─────────────────────┐
                    │   Orchestrator      │
                    │   (port 8000)       │
                    └──────────┬──────────┘
                               │ A2A
          ┌────────────────────┼────────────────────┐
          │    │    │    │    │    │    │    │    │    │
        8001 8002 8003 8004 8005 8006 8007 8008 8009 8010
        Acct  Txn Loan Card Fraud KYC  Inv  Ins  Supp Audit
          │    │    │    │    │    │    │    │    │    │
        9001 9002 9003 9004 9005 9006 9007 9008 9009 9010
         └── MCP Servers (stdio, started automatically) ──┘
```

## Agents

| # | Agent | Port | MCP Server | Domain |
|---|-------|------|------------|--------|
| 1 | Account Management | 8001 | account_db (9001) | Accounts, balances |
| 2 | Transaction Processing | 8002 | transaction_engine (9002) | Transfers, payments |
| 3 | Loan Management | 8003 | loan_engine (9003) | Loans, EMI, schedules |
| 4 | Card Services | 8004 | card_system (9004) | Credit/debit cards |
| 5 | Fraud Detection | 8005 | fraud_engine (9005) | Risk scoring, alerts |
| 6 | KYC Compliance | 8006 | kyc_registry (9006) | Identity, AML |
| 7 | Investment Portfolio | 8007 | market_data (9007) | Stocks, portfolio |
| 8 | Insurance Services | 8008 | insurance_engine (9008) | Policies, claims |
| 9 | Customer Support | 8009 | support_ticketing (9009) | Tickets, FAQs |
| 10 | Audit Compliance | 8010 | audit_ledger (9010) | Audit trails, regulations |

## Setup

```bash
# 1. Install dependencies
pip install -e .
# or
make install

# 2. Copy and configure environment
cp .env.example .env
# Edit .env with your GOOGLE_API_KEY

# 3. Launch everything
make run
# or
./launch_all.sh
```

## Usage

The orchestrator runs on **http://localhost:8000** and accepts natural language requests. It routes to the correct specialist agent automatically.

**Example requests:**
- "What is the balance of account ACC-1001?"
- "Transfer $500 from ACC-1001 to ACC-1002"
- "Apply for a home loan of $200,000 for account ACC-1001"
- "Block card CARD-3001 — it was stolen"
- "Check if my KYC is complete for ACC-1002"

## Project Structure

```
bank-finance-system/
├── orchestrator.py          # Central orchestrator (port 8000)
├── agents/                  # 10 A2A specialist agents
│   ├── account_management_agent.py
│   ├── transaction_processing_agent.py
│   ├── loan_management_agent.py
│   ├── card_services_agent.py
│   ├── fraud_detection_agent.py
│   ├── kyc_compliance_agent.py
│   ├── investment_portfolio_agent.py
│   ├── insurance_services_agent.py
│   ├── customer_support_agent.py
│   └── audit_compliance_agent.py
├── mcp_servers/             # 10 MCP tool servers
│   ├── account_db_server.py
│   ├── transaction_engine_server.py
│   ├── loan_engine_server.py
│   ├── card_system_server.py
│   ├── fraud_engine_server.py
│   ├── kyc_registry_server.py
│   ├── market_data_server.py
│   ├── insurance_engine_server.py
│   ├── support_ticketing_server.py
│   └── audit_ledger_server.py
├── DESIGN_SPEC.md
├── pyproject.toml
├── .env.example
├── launch_all.sh
├── Makefile
└── README.md
```

## Requirements

- Python 3.11+
- Google AI API key (for Gemini model)
- `google-adk[a2a]>=1.0.0`
- `mcp>=1.0.0`
