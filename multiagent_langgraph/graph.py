"""LangGraph StateGraph — wires the 4 agents into a sequential pipeline.

Pipeline:  START → search → research → analysis → writer → END
"""

from langgraph.graph import StateGraph, START, END

from .state import AgentState
from .agents.search_agent import search_node
from .agents.research_agent import research_node
from .agents.analysis_agent import analysis_node
from .agents.writer_agent import writer_node


def build_graph():
    """Build and compile the multiagent research pipeline."""
    builder = StateGraph(AgentState)

    # --- Register nodes ---
    builder.add_node("search", search_node)
    builder.add_node("research", research_node)
    builder.add_node("analysis", analysis_node)
    builder.add_node("writer", writer_node)

    # --- Sequential pipeline edges ---
    builder.add_edge(START, "search")
    builder.add_edge("search", "research")
    builder.add_edge("research", "analysis")
    builder.add_edge("analysis", "writer")
    builder.add_edge("writer", END)

    return builder.compile()


# Module-level compiled graph — import this in main.py
graph = build_graph()
