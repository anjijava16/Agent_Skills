# DESIGN_SPEC.md — Multi-Agent Bank Finance System

## Overview

A multi-agent banking finance system built with Google ADK, featuring 10 specialized
agents exposed as A2A (Agent-to-Agent) servers, 10 MCP (Model Context Protocol) servers
providing domain-specific tooling, and 1 orchestrator agent that coordinates all agents.

Each specialist agent runs as an independent A2A service on its own port, connects to
its dedicated MCP server for domain tools, and registers with the central orchestrator.
The orchestrator uses `RemoteA2aAgent` to delegate requests to the appropriate specialist
based on user intent.

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                   ORCHESTRATOR AGENT                     │
│              (Port 8000 — Central Router)                │
│  Routes to specialists via RemoteA2aAgent connections    │
└──────┬──┬──┬──┬──┬──┬──┬──┬──┬──┬───────────────────────┘
       │  │  │  │  │  │  │  │  │  │
  ┌────┘  │  │  │  │  │  │  │  │  └────┐
  ▼       ▼  ▼  ▼  ▼  ▼  ▼  ▼  ▼      ▼
┌─────┐┌─────┐┌─────┐┌─────┐┌─────┐┌─────┐┌─────┐┌─────┐┌─────┐┌─────┐
│Acct ││Txn  ││Loan ││Card ││Fraud││KYC  ││Inv  ││Ins  ││Supp ││Audit│
│Mgmt ││Proc ││Mgmt ││Serv ││Det  ││Comp ││Port ││Serv ││Cust ││Compl│
│:8001││:8002││:8003││:8004││:8005││:8006││:8007││:8008││:8009││:8010│
└──┬──┘└──┬──┘└──┬──┘└──┬──┘└──┬──┘└──┬──┘└──┬──┘└──┬──┘└──┬──┘└──┬──┘
   │      │      │      │      │      │      │      │      │      │
   ▼      ▼      ▼      ▼      ▼      ▼      ▼      ▼      ▼      ▼
┌─────┐┌─────┐┌─────┐┌─────┐┌─────┐┌─────┐┌─────┐┌─────┐┌─────┐┌─────┐
│MCP  ││MCP  ││MCP  ││MCP  ││MCP  ││MCP  ││MCP  ││MCP  ││MCP  ││MCP  │
│9001 ││9002 ││9003 ││9004 ││9005 ││9006 ││9007 ││9008 ││9009 ││9010 │
└─────┘└─────┘└─────┘└─────┘└─────┘└─────┘└─────┘└─────┘└─────┘└─────┘
```

## The 10 Agents (A2A Servers)

| # | Agent Name | Port | Description | MCP Server |
|---|-----------|------|-------------|------------|
| 1 | Account Management | 8001 | Create/read/update accounts, balance inquiries | MCP Account DB (9001) |
| 2 | Transaction Processing | 8002 | Transfers, payments, deposits, withdrawals | MCP Transaction Engine (9002) |
| 3 | Loan Management | 8003 | Loan applications, approvals, EMI calculations | MCP Loan Engine (9003) |
| 4 | Card Services | 8004 | Credit/debit card issue, block, limits, rewards | MCP Card System (9004) |
| 5 | Fraud Detection | 8005 | Transaction monitoring, suspicious activity alerts | MCP Fraud Engine (9005) |
| 6 | KYC & Compliance | 8006 | Identity verification, document checks, AML | MCP KYC Registry (9006) |
| 7 | Investment Portfolio | 8007 | Buy/sell stocks, mutual funds, portfolio tracking | MCP Market Data (9007) |
| 8 | Insurance Services | 8008 | Policy quotes, claims, coverage management | MCP Insurance Engine (9008) |
| 9 | Customer Support | 8009 | FAQs, complaints, ticket management, escalation | MCP Support Ticketing (9009) |
| 10| Audit & Compliance | 8010 | Audit trails, regulatory reports, compliance checks | MCP Audit Ledger (9010) |

## The 10 MCP Servers

Each MCP server provides domain-specific tools via stdio transport:

| # | MCP Server | Port | Tools Provided |
|---|-----------|------|----------------|
| 1 | Account DB | 9001 | get_account, create_account, update_account, get_balance, list_accounts |
| 2 | Transaction Engine | 9002 | process_transfer, process_payment, get_transaction_history, get_statement |
| 3 | Loan Engine | 9003 | apply_loan, get_loan_status, calculate_emi, get_loan_schedule, approve_loan |
| 4 | Card System | 9004 | issue_card, block_card, set_card_limit, get_card_details, get_rewards_balance |
| 5 | Fraud Engine | 9005 | check_transaction_risk, flag_suspicious, get_fraud_alerts, verify_transaction |
| 6 | KYC Registry | 9006 | verify_identity, check_documents, get_kyc_status, run_aml_check, submit_kyc |
| 7 | Market Data | 9007 | get_stock_price, get_portfolio, buy_stock, sell_stock, get_market_summary |
| 8 | Insurance Engine | 9008 | get_policy_quote, create_policy, file_claim, get_claim_status, list_policies |
| 9 | Support Ticketing | 9009 | create_ticket, get_ticket_status, update_ticket, search_faq, escalate_ticket |
| 10| Audit Ledger | 9010 | log_audit_event, get_audit_trail, generate_report, check_compliance, get_regulations |

## Example Use Cases

1. **Balance Inquiry**: User asks "What's my account balance?" → Orchestrator routes to Account Management Agent → Agent calls MCP Account DB `get_balance` tool
2. **Money Transfer**: User says "Transfer $500 to John" → Orchestrator routes to Transaction Processing → Fraud Detection check → Transaction executed
3. **Loan Application**: User requests "I want a home loan of $200,000" → Orchestrator routes to Loan Management → EMI calculated, credit check via KYC
4. **Report Fraud**: User reports "I see unauthorized charges" → Orchestrator routes to Fraud Detection → Alert created, card blocked via Card Services
5. **Investment Trade**: User says "Buy 10 shares of AAPL" → Orchestrator routes to Investment Portfolio → Market data checked, trade executed

## Constraints & Safety Rules

1. All financial transactions MUST be logged to the Audit Ledger
2. Transfers above $10,000 require human approval (tool confirmation)
3. Agents must NEVER reveal internal system details or customer data of other users
4. Fraud detection must run before processing high-value transactions
5. KYC verification required before opening new accounts or issuing loans
6. All MCP servers use simulated in-memory data (no real banking connections)
7. Sensitive operations (block card, approve loan) require explicit confirmation

## Success Criteria

1. All 10 agents start as independent A2A services
2. All 10 MCP servers provide their tools correctly
3. Orchestrator correctly routes requests to appropriate specialist agents
4. End-to-end flows work (e.g., open account → transfer → check balance)
5. Each agent's tools are accessible and return proper responses

## Edge Cases

1. User asks about something no agent handles → Orchestrator responds with available services
2. MCP server down → Agent returns graceful error
3. Ambiguous requests → Orchestrator asks for clarification
4. Multi-step workflows → Orchestrator chains multiple agents
5. Invalid account/transaction data → Proper validation errors returned
