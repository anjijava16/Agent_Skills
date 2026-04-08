#!/usr/bin/env bash
# launch_all.sh — Start all 10 A2A agents then the orchestrator.
# MCP servers are started automatically by each agent via StdioConnectionParams.
#
# Usage:  ./launch_all.sh
# Stop:   Ctrl-C (sends SIGINT to the process group)
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

# Load .env if present
if [ -f .env ]; then
  set -a; source .env; set +a
fi

PIDS=()

cleanup() {
  echo ""
  echo "🛑 Shutting down all agents..."
  for pid in "${PIDS[@]}"; do
    kill "$pid" 2>/dev/null || true
  done
  wait 2>/dev/null
  echo "✅ All agents stopped."
}
trap cleanup EXIT INT TERM

echo "🏦 Bank Finance Multi-Agent System — Starting..."
echo ""

# --- Start 10 specialist A2A agents ---
AGENTS=(
  "agents/account_management_agent.py"
  "agents/transaction_processing_agent.py"
  "agents/loan_management_agent.py"
  "agents/card_services_agent.py"
  "agents/fraud_detection_agent.py"
  "agents/kyc_compliance_agent.py"
  "agents/investment_portfolio_agent.py"
  "agents/insurance_services_agent.py"
  "agents/customer_support_agent.py"
  "agents/audit_compliance_agent.py"
)

PORTS=(8001 8002 8003 8004 8005 8006 8007 8008 8009 8010)

for i in "${!AGENTS[@]}"; do
  echo "  ▶ Starting ${AGENTS[$i]} on port ${PORTS[$i]}..."
  python "${AGENTS[$i]}" &
  PIDS+=($!)
done

# Give agents a moment to bind their ports
echo ""
echo "⏳ Waiting for agents to initialize..."
sleep 3

# --- Start orchestrator ---
echo "  ▶ Starting orchestrator on port ${ORCHESTRATOR_PORT:-8000}..."
python orchestrator.py &
PIDS+=($!)

echo ""
echo "✅ All services running!"
echo "   Orchestrator: http://localhost:${ORCHESTRATOR_PORT:-8000}"
echo "   Agents:       http://localhost:8001 — http://localhost:8010"
echo ""
echo "Press Ctrl-C to stop all services."

# Wait for all background processes
wait
