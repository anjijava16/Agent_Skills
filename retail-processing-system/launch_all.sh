#!/usr/bin/env bash
# ============================================================================
# launch_all.sh — Start the entire Retail Processing multi-agent system.
#
# Order: FastMCP SSE servers → A2A agents → orchestrator
# FastMCP servers must be running BEFORE agents connect to them.
# ============================================================================
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

# Load env vars if .env exists
[[ -f .env ]] && set -a && source .env && set +a

PIDS=()
cleanup() {
    echo ""
    echo "🛑 Shutting down all processes..."
    for pid in "${PIDS[@]}"; do
        kill "$pid" 2>/dev/null || true
    done
    wait 2>/dev/null
    echo "✅ All processes stopped."
}
trap cleanup EXIT INT TERM

start_bg() {
    local label="$1"; shift
    echo "  ▶ $label"
    "$@" &
    PIDS+=($!)
    sleep 0.3
}

# ============================================================================
# Phase 1: Start all 10 FastMCP SSE servers
# ============================================================================
echo ""
echo "═══════════════════════════════════════════════════════"
echo "  Phase 1/3 — Starting 10 FastMCP MCP Servers (SSE)"
echo "═══════════════════════════════════════════════════════"

start_bg "Product Catalog  MCP (9001)" python -m mcp_servers.product_catalog_server
start_bg "Order Engine     MCP (9002)" python -m mcp_servers.order_engine_server
start_bg "Inventory        MCP (9003)" python -m mcp_servers.inventory_server
start_bg "Customer DB      MCP (9004)" python -m mcp_servers.customer_db_server
start_bg "Payment Gateway  MCP (9005)" python -m mcp_servers.payment_gateway_server
start_bg "Shipping         MCP (9006)" python -m mcp_servers.shipping_server
start_bg "Promotions       MCP (9007)" python -m mcp_servers.promotions_server
start_bg "Returns          MCP (9008)" python -m mcp_servers.returns_server
start_bg "Analytics        MCP (9009)" python -m mcp_servers.analytics_server
start_bg "Supplier         MCP (9010)" python -m mcp_servers.supplier_server

echo ""
echo "⏳ Waiting 3s for MCP servers to become ready..."
sleep 3

# ============================================================================
# Phase 2: Start all 10 A2A agents
# ============================================================================
echo ""
echo "═══════════════════════════════════════════════════════"
echo "  Phase 2/3 — Starting 10 A2A Specialist Agents"
echo "═══════════════════════════════════════════════════════"

start_bg "Product Catalog  Agent (8001)" python -m agents.product_catalog_agent
start_bg "Order Processing Agent (8002)" python -m agents.order_processing_agent
start_bg "Inventory Mgmt   Agent (8003)" python -m agents.inventory_management_agent
start_bg "Customer Mgmt    Agent (8004)" python -m agents.customer_management_agent
start_bg "Payment          Agent (8005)" python -m agents.payment_processing_agent
start_bg "Shipping         Agent (8006)" python -m agents.shipping_logistics_agent
start_bg "Promotions       Agent (8007)" python -m agents.promotions_pricing_agent
start_bg "Returns          Agent (8008)" python -m agents.returns_refunds_agent
start_bg "Analytics        Agent (8009)" python -m agents.analytics_reporting_agent
start_bg "Supplier Mgmt    Agent (8010)" python -m agents.supplier_management_agent

echo ""
echo "⏳ Waiting 3s for agents to connect to MCP servers..."
sleep 3

# ============================================================================
# Phase 3: Start the orchestrator
# ============================================================================
echo ""
echo "═══════════════════════════════════════════════════════"
echo "  Phase 3/3 — Starting Orchestrator"
echo "═══════════════════════════════════════════════════════"

start_bg "Retail Orchestrator (8000)" python -m orchestrator

echo ""
echo "═══════════════════════════════════════════════════════"
echo "  🚀 Retail Processing System — ALL SERVICES RUNNING"
echo "═══════════════════════════════════════════════════════"
echo ""
echo "  Orchestrator:  http://localhost:${ORCHESTRATOR_PORT:-8000}"
echo "  Agent Card:    http://localhost:${ORCHESTRATOR_PORT:-8000}/.well-known/agent.json"
echo ""
echo "  Press Ctrl+C to shut down everything."
echo ""

wait
