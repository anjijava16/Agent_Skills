"""Entry point for the multiagent LangGraph research pipeline.

Usage:
    python main.py "Quantum Computing"
    python main.py                         # prompts for topic interactively

Output:
    A markdown report saved to outputs/<topic>_<timestamp>.md
"""

import os
import sys

from dotenv import load_dotenv

# Load OPENAI_API_KEY from .env (if present)
load_dotenv()

from multiagent_langgraph.graph import graph  # noqa: E402  (after load_dotenv)


STEP_LABELS = {
    "search":   "🔍 Search Agent   — gathering information",
    "research": "📚 Research Agent — deep-diving the topic",
    "analysis": "🧠 Analysis Agent — synthesising insights",
    "writer":   "✍️  Writer Agent   — composing markdown report",
}


def run(topic: str) -> str:
    """Run the full pipeline for *topic* and return the output file path."""
    print(f"\n{'=' * 62}")
    print(f"  Multiagent LangGraph Research Pipeline")
    print(f"  Topic: {topic}")
    print(f"{'=' * 62}\n")

    initial_state = {
        "topic": topic,
        "search_results": "",
        "research_data": "",
        "analysis": "",
        "output_file": "",
    }

    output_file = ""

    # stream() yields {node_name: state_update} for each completed node
    for chunk in graph.stream(initial_state):
        for node_name, updates in chunk.items():
            label = STEP_LABELS.get(node_name, f"⚙️  {node_name}")
            print(f"\n✅ {label}")

            if updates.get("output_file"):
                output_file = updates["output_file"]

    print(f"\n{'=' * 62}")
    print(f"  Pipeline complete!")
    if output_file:
        print(f"  📄 Report saved → {output_file}")
    print(f"{'=' * 62}\n")

    return output_file


if __name__ == "__main__":
    if not os.getenv("OPENAI_API_KEY"):
        print("❌  OPENAI_API_KEY not set. Create a .env file or export the variable.")
        sys.exit(1)

    if len(sys.argv) >= 2:
        topic_input = " ".join(sys.argv[1:])
    else:
        topic_input = input("Enter research topic: ").strip()
        if not topic_input:
            topic_input = "Artificial Intelligence in Healthcare"

    run(topic_input)
