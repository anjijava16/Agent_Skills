"""Writer Agent — composes the final markdown report and saves it to disk."""

import os
import re
from datetime import datetime

from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage

from ..state import AgentState

MODEL = "gpt-4o"
OUTPUT_DIR = "outputs"


def _safe_filename(topic: str) -> str:
    """Convert a topic string to a safe filename."""
    name = topic.lower().strip()
    name = re.sub(r"[^a-z0-9\s_-]", "", name)
    name = re.sub(r"\s+", "_", name)
    return name[:80]  # cap length


def writer_node(state: AgentState) -> dict:
    """Node 4 — Write a polished markdown report and save it as <topic>.md."""
    print(f"  [writer_agent] Writing report for: {state['topic']}")

    llm = ChatOpenAI(model=MODEL, temperature=0.5)

    messages = [
        SystemMessage(
            content=(
                "You are an expert technical writer and editor. "
                "Using the research and analysis provided, write a complete, "
                "polished markdown document. The document MUST include:\n\n"
                "  1. A clear title (# heading)\n"
                "  2. An executive summary / abstract\n"
                "  3. Table of contents\n"
                "  4. Introduction — why this topic matters\n"
                "  5. Key Findings — detailed sections based on the research\n"
                "  6. Analysis & Insights — synthesised from the analysis data\n"
                "  7. Conclusions & Recommendations\n"
                "  8. Further Reading / References (suggested)\n\n"
                "Use proper markdown: headers, bullet lists, bold for emphasis, "
                "horizontal rules between major sections. "
                "The report should be comprehensive, well-written, and publication-ready."
            )
        ),
        HumanMessage(
            content=(
                f"Topic: {state['topic']}\n\n"
                f"## Search Results\n{state['search_results']}\n\n"
                f"## Research Data\n{state['research_data']}\n\n"
                f"## Analysis\n{state['analysis']}\n\n"
                "Write a comprehensive, well-formatted markdown report on this topic."
            )
        ),
    ]

    response = llm.invoke(messages)
    markdown_content = response.content

    # Ensure outputs directory exists
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    filename = _safe_filename(state["topic"])
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = os.path.join(OUTPUT_DIR, f"{filename}_{timestamp}.md")

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(markdown_content)

    print(f"  [writer_agent] Saved report → {output_path}")
    return {"output_file": output_path}
