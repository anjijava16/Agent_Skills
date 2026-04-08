.PHONY: install run stop test clean

install:
	uv pip install -e ".[dev]" 2>/dev/null || pip install -e "."

run:
	@chmod +x launch_all.sh
	./launch_all.sh

# Run the orchestrator only (assumes agents are already running)
run-orchestrator:
	python orchestrator.py

# Run a single agent (example: make run-agent AGENT=account_management_agent)
run-agent:
	python agents/$(AGENT).py

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
