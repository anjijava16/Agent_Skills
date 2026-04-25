"""Shared state schema for the multiagent pipeline."""

from typing_extensions import TypedDict


class AgentState(TypedDict):
    """State passed between all agents in the pipeline."""

    topic: str            # Input research topic
    search_results: str   # Output from search_agent
    research_data: str    # Output from research_agent
    analysis: str         # Output from analysis_agent
    output_file: str      # Path to written .md file
