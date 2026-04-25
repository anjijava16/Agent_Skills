# Multiagent LangGraph Research Pipeline

A 4-agent sequential pipeline built with **LangGraph** that:

1. **Search Agent** — gathers key facts, figures, and concepts on any topic  
2. **Research Agent** — deep-dives into the topic using the search results  
3. **Analysis Agent** — synthesises insights, patterns, and recommendations  
4. **Writer Agent** — composes a polished markdown report and saves it to `outputs/`

---

## Architecture

```
START → search → research → analysis → writer → END
```

Each agent is a LangGraph node that reads from and writes to a shared `AgentState` TypedDict. The pipeline runs sequentially, with each node's output becoming the next node's input.

```
AgentState
├── topic           str   ← input
├── search_results  str   ← set by search_agent
├── research_data   str   ← set by research_agent
├── analysis        str   ← set by analysis_agent
└── output_file     str   ← set by writer_agent (path to .md file)
```

---

## Project Structure

```
multiagent_langgraph/
├── __init__.py
├── state.py              # AgentState TypedDict
├── graph.py              # StateGraph wiring
├── main.py               # Entry point
├── agents/
│   ├── __init__.py
│   ├── search_agent.py   # Node 1 — search
│   ├── research_agent.py # Node 2 — research
│   ├── analysis_agent.py # Node 3 — analysis
│   └── writer_agent.py   # Node 4 — write .md file
├── outputs/              # Generated markdown reports (created at runtime)
├── requirements.txt
└── .env.example
```

---

## Setup

### 1. Install dependencies

```bash
cd multiagent_langgraph
pip install -r requirements.txt
```

### 2. Configure API key

```bash
cp .env.example .env
# Edit .env and set your OPENAI_API_KEY
```

### 3. Run the pipeline

```bash
# Pass topic as argument
python main.py "Quantum Computing"

# Or run interactively
python main.py
```

The markdown report is saved to `outputs/<topic>_<timestamp>.md`.

---

## Model

All agents use `gpt-4o` by default. To switch models, change the `MODEL` constant at the top of each agent file:

```python
# agents/search_agent.py  (and other agent files)
MODEL = "gpt-4o"        # current default
# MODEL = "gpt-5"       # switch when available on your OpenAI account
```

---

## Example Output

Running:
```bash
python main.py "Artificial Intelligence in Healthcare"
```

Produces:
```
outputs/artificial_intelligence_in_healthcare_20240601_143022.md
```

Containing a full markdown report with title, executive summary, table of contents, key findings, analysis, and recommendations.

---

## Extending the Pipeline

### Add a new agent node

1. Create `agents/my_agent.py` with a `my_node(state: AgentState) -> dict` function  
2. Register it in `graph.py`:

```python
builder.add_node("my_node", my_node)
builder.add_edge("analysis", "my_node")
builder.add_edge("my_node", "writer")
```

3. Add the new field to `AgentState` in `state.py` if the node produces new data.

### Enable web search (Tavily)

Install `langchain-community` and `tavily-python`, then replace the LLM call in `search_agent.py` with a `TavilySearchResults` tool call for real-time web data.

```python
from langchain_community.tools.tavily_search import TavilySearchResults
tool = TavilySearchResults(max_results=5)
results = tool.invoke(state["topic"])
```

---

## Requirements

| Package | Min Version |
|---|---|
| langgraph | 0.2.0 |
| langchain | 0.3.0 |
| langchain-openai | 0.2.0 |
| langchain-core | 0.3.0 |
| python-dotenv | 1.0.0 |
