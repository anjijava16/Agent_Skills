# Retail Processing Multi-Agent System

A **10-agent, 10-MCP-server** retail processing platform built with **Google ADK (A2A)** and **FastMCP (SSE)**.

## Architecture

```
┌────────────────────────────────────────────────────────────┐
│                   ORCHESTRATOR (port 8000)                  │
│          Routes requests to specialist agents               │
└──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬─────────────────────────────┘
   │  │  │  │  │  │  │  │  │  │  A2A Protocol
   ▼  ▼  ▼  ▼  ▼  ▼  ▼  ▼  ▼  ▼
┌─────┐┌─────┐┌─────┐┌─────┐┌─────┐┌─────┐┌─────┐┌─────┐┌─────┐┌─────┐
│8001 ││8002 ││8003 ││8004 ││8005 ││8006 ││8007 ││8008 ││8009 ││8010 │
│Prod ││Order││Inv  ││Cust ││Pay  ││Ship ││Promo││Ret  ││Analy││Supp │
│Cat  ││Proc ││Mgmt ││Mgmt ││Proc ││Log  ││Price││Ref  ││Rep  ││Mgmt │
└──┬──┘└──┬──┘└──┬──┘└──┬──┘└──┬──┘└──┬──┘└──┬──┘└──┬──┘└──┬──┘└──┬──┘
   │      │      │      │      │      │      │      │      │      │
   ▼      ▼      ▼      ▼      ▼      ▼      ▼      ▼      ▼      ▼
┌─────┐┌─────┐┌─────┐┌─────┐┌─────┐┌─────┐┌─────┐┌─────┐┌─────┐┌─────┐
│9001 ││9002 ││9003 ││9004 ││9005 ││9006 ││9007 ││9008 ││9009 ││9010 │
│Prod ││Order││Inv  ││Cust ││Pay  ││Ship ││Promo││Ret  ││Analy││Supp │
│MCP  ││MCP  ││MCP  ││MCP  ││MCP  ││MCP  ││MCP  ││MCP  ││MCP  ││MCP  │
└─────┘└─────┘└─────┘└─────┘└─────┘└─────┘└─────┘└─────┘└─────┘└─────┘
         FastMCP SSE Servers (persistent HTTP processes)
```

## Components

### 10 FastMCP Servers (SSE Transport)

| # | Server | Port | Tools |
|---|--------|------|-------|
| 1 | Product Catalog | 9001 | get_product, search_products, list_categories, create_product, update_product |
| 2 | Order Engine | 9002 | create_order, get_order, update_order_status, cancel_order, get_order_history |
| 3 | Inventory | 9003 | check_stock, update_stock, get_low_stock_alerts, reserve_stock, release_stock |
| 4 | Customer DB | 9004 | get_customer, create_customer, update_customer, get_loyalty_points, search_customers |
| 5 | Payment Gateway | 9005 | process_payment, refund_payment, get_payment_status, list_transactions, verify_payment |
| 6 | Shipping | 9006 | create_shipment, track_shipment, get_shipping_rates, update_delivery, list_carriers |
| 7 | Promotions | 9007 | apply_coupon, get_active_promotions, calculate_discount, create_promotion, validate_coupon |
| 8 | Returns | 9008 | initiate_return, get_return_status, approve_return, process_refund, list_returns |
| 9 | Analytics | 9009 | get_sales_summary, get_top_products, get_revenue_report, get_customer_metrics, get_inventory_turnover |
| 10 | Supplier | 9010 | get_supplier, create_purchase_order, get_po_status, list_suppliers, update_supplier |

### 10 A2A Agents

| # | Agent | Port | MCP |
|---|-------|------|-----|
| 1 | Product Catalog Agent | 8001 | → 9001 |
| 2 | Order Processing Agent | 8002 | → 9002 |
| 3 | Inventory Management Agent | 8003 | → 9003 |
| 4 | Customer Management Agent | 8004 | → 9004 |
| 5 | Payment Processing Agent | 8005 | → 9005 |
| 6 | Shipping & Logistics Agent | 8006 | → 9006 |
| 7 | Promotions & Pricing Agent | 8007 | → 9007 |
| 8 | Returns & Refunds Agent | 8008 | → 9008 |
| 9 | Analytics & Reporting Agent | 8009 | → 9009 |
| 10 | Supplier Management Agent | 8010 | → 9010 |

## Quick Start

```bash
# 1. Install dependencies
pip install -e .

# 2. Copy and configure environment
cp .env.example .env
# Edit .env with your GOOGLE_API_KEY

# 3. Launch everything
chmod +x launch_all.sh
./launch_all.sh
```

## Usage

### With Makefile

```bash
make install     # Install dependencies
make run         # Start all services
make run-mcp     # Start only MCP servers (dev mode)
make stop        # Kill all services on default ports
make clean       # Remove caches
```

### Example Requests

Once running, send requests to the orchestrator at `http://localhost:8000`:

- *"Search for wireless headphones in the catalog"*
- *"Place an order for 2x SKU-1001 for customer CUST-100"*
- *"Check inventory for SKU-1003 and alert if low"*
- *"Apply coupon SAVE10 to an order of $150"*
- *"What were last month's top-selling products?"*

## Technology Stack

- **Google ADK** (`google-adk[a2a]`) — Agent framework + A2A protocol
- **FastMCP** (`fastmcp`) — MCP servers with `@mcp.tool()` decorators + SSE transport
- **Model**: `gemini-3-flash-preview`
- **Python**: 3.11+

## Port Map

| Range | Purpose |
|-------|---------|
| 8000 | Orchestrator |
| 8001–8010 | A2A Specialist Agents |
| 9001–9010 | FastMCP SSE Servers |
