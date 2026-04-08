# Retail Processing Multi-Agent System — Design Specification

## Overview

A multi-agent retail processing system built with **Google ADK**, **FastMCP**, and **A2A** protocol.
10 specialist agents handle distinct retail domains, each backed by a FastMCP tool server
running over SSE transport. A single orchestrator routes customer/staff requests to the
appropriate specialist via A2A.

## Architecture

```
                 ┌──────────────────────────┐
                 │   Retail Orchestrator     │
                 │   (A2A — port 8000)      │
                 └────────────┬─────────────┘
                              │ A2A (RemoteA2aAgent)
    ┌──────┬──────┬──────┬────┴───┬──────┬──────┬──────┬──────┬──────┐
  8001   8002   8003   8004   8005   8006   8007   8008   8009   8010
  Prod   Order  Invnt  Cust   Pay    Ship   Promo  Retrn  Anlyt  Suppl
    │      │      │      │      │      │      │      │      │      │
  9001   9002   9003   9004   9005   9006   9007   9008   9009   9010
    └─────── FastMCP Servers (SSE transport) ──────────────────────┘
```

## 10 Agents (A2A Servers)

| # | Agent                    | Port | Description                                    |
|---|--------------------------|------|------------------------------------------------|
| 1 | Product Catalog          | 8001 | Product search, details, categories, CRUD      |
| 2 | Order Processing         | 8002 | Create, track, update, cancel orders           |
| 3 | Inventory Management     | 8003 | Stock levels, alerts, reservations              |
| 4 | Customer Management      | 8004 | Profiles, loyalty, preferences, search          |
| 5 | Payment Processing       | 8005 | Payments, refunds, transaction history          |
| 6 | Shipping & Logistics     | 8006 | Shipments, tracking, rates, carriers            |
| 7 | Promotions & Pricing     | 8007 | Coupons, discounts, active promotions           |
| 8 | Returns & Refunds        | 8008 | Return initiation, approval, refund processing  |
| 9 | Analytics & Reporting    | 8009 | Sales, revenue, top products, customer metrics  |
| 10| Supplier Management      | 8010 | Suppliers, purchase orders, restocking          |

## 10 MCP Servers (FastMCP over SSE)

| # | Server                   | Port | Tools                                                          |
|---|--------------------------|------|----------------------------------------------------------------|
| 1 | product_catalog_server   | 9001 | get_product, search_products, list_categories, create_product, update_product |
| 2 | order_engine_server      | 9002 | create_order, get_order, update_order_status, cancel_order, get_order_history |
| 3 | inventory_server         | 9003 | check_stock, update_stock, get_low_stock_alerts, reserve_stock, release_stock |
| 4 | customer_db_server       | 9004 | get_customer, create_customer, update_customer, get_loyalty_points, search_customers |
| 5 | payment_gateway_server   | 9005 | process_payment, refund_payment, get_payment_status, list_transactions, verify_payment |
| 6 | shipping_server          | 9006 | create_shipment, track_shipment, get_shipping_rates, update_delivery, list_carriers |
| 7 | promotions_server        | 9007 | apply_coupon, get_active_promotions, calculate_discount, create_promotion, validate_coupon |
| 8 | returns_server           | 9008 | initiate_return, get_return_status, approve_return, process_refund, list_returns |
| 9 | analytics_server         | 9009 | get_sales_summary, get_top_products, get_revenue_report, get_customer_metrics, get_inventory_turnover |
| 10| supplier_server          | 9010 | get_supplier, create_purchase_order, get_po_status, list_suppliers, update_supplier |

## Port Map

- **8000** — Orchestrator (A2A)
- **8001–8010** — Specialist agents (A2A)
- **9001–9010** — FastMCP tool servers (SSE)

## Example Use Cases

1. **"Show me product SKU-1001"** → Product Catalog agent → product_catalog_server
2. **"Place an order for 3 units of SKU-1001 for customer CUST-100"** → Order Processing → Inventory (reserve) → Payment
3. **"Track my shipment SHIP-5001"** → Shipping & Logistics agent
4. **"Apply coupon SAVE20 to order ORD-2001"** → Promotions agent
5. **"What were top-selling products last month?"** → Analytics agent

## Technology Stack

- **Google ADK** `google-adk[a2a]>=1.0.0` — agents, A2A, RemoteA2aAgent
- **FastMCP** `fastmcp>=2.0.0` — MCP servers with `@mcp.tool()` decorators, SSE transport
- **Model** — `gemini-3-flash-preview` (do not change)
- **Python** 3.11+

## Constraints

- All MCP servers use FastMCP with SSE transport (not stdio)
- Agents connect to MCP servers via `SseConnectionParams`
- In-memory data stores (no external DB required for demo)
- Orchestrator uses `RemoteA2aAgent` to reach all 10 specialists
