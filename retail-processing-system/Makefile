# ============================================================================
# Retail Processing System — Makefile
# ============================================================================

.PHONY: install run stop test clean

# Install all dependencies
install:
	pip install -e ".[dev]"

# Start the full system (MCP servers → agents → orchestrator)
run:
	chmod +x launch_all.sh && ./launch_all.sh

# Start only MCP servers (useful for development)
run-mcp:
	@echo "Starting 10 FastMCP servers..."
	python -m mcp_servers.product_catalog_server &
	python -m mcp_servers.order_engine_server &
	python -m mcp_servers.inventory_server &
	python -m mcp_servers.customer_db_server &
	python -m mcp_servers.payment_gateway_server &
	python -m mcp_servers.shipping_server &
	python -m mcp_servers.promotions_server &
	python -m mcp_servers.returns_server &
	python -m mcp_servers.analytics_server &
	python -m mcp_servers.supplier_server &
	@echo "All MCP servers started."

# Stop all processes on the default ports
stop:
	@echo "Stopping all processes..."
	@for port in 8000 8001 8002 8003 8004 8005 8006 8007 8008 8009 8010 \
	             9001 9002 9003 9004 9005 9006 9007 9008 9009 9010; do \
		lsof -ti:$$port | xargs kill -9 2>/dev/null || true; \
	done
	@echo "Done."

# Remove caches
clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	rm -rf *.egg-info .pytest_cache
