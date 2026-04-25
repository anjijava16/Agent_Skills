"""Research Agent — deep-dives the topic using search results."""

from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage

from ..state import AgentState

MODEL = "gpt-4o"


def research_node(state: AgentState) -> dict:
    """Node 2 — Deepen the research based on initial search results."""
    print(f"  [research_agent] Deep-researching: {state['topic']}")

    llm = ChatOpenAI(model=MODEL, temperature=0.3)

    messages = [
        SystemMessage(
            content=(
                "You are a deep research specialist. "
                "Given a topic and initial search results, conduct an in-depth investigation that covers:\n"
                "  - Historical background and evolution\n"
                "  - Technical or scientific details\n"
                "  - Case studies or real-world examples\n"
                "  - Controversies, debates, or open questions\n"
                "  - Expert opinions and academic perspectives\n"
                "  - Future directions and implications\n\n"
                "Organise findings in clearly labelled sub-sections. "
                "Build on the search results — do not simply repeat them."
            )
        ),
        HumanMessage(
            content=(
                f"Topic: {state['topic']}\n\n"
                f"Initial Search Results:\n{state['search_results']}\n\n"
                "Conduct a deep research investigation and provide comprehensive, "
                "well-organised findings that go beyond the initial search."
            )
        ),
    ]

    response = llm.invoke(messages)
    return {"research_data": response.content}
