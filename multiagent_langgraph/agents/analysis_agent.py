"""Analysis Agent — synthesises and critically analyses the research data."""

from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage

from ..state import AgentState

MODEL = "gpt-4o"


def analysis_node(state: AgentState) -> dict:
    """Node 3 — Analyse and synthesise all gathered research into key insights."""
    print(f"  [analysis_agent] Analysing: {state['topic']}")

    llm = ChatOpenAI(model=MODEL, temperature=0.4)

    messages = [
        SystemMessage(
            content=(
                "You are a senior analyst and critical thinker. "
                "Given a topic and its research data, produce a rigorous analysis that includes:\n"
                "  - Summary of the most important findings\n"
                "  - Patterns, themes, and connections across the data\n"
                "  - Strengths, weaknesses, opportunities, and threats (SWOT)\n"
                "  - Critical evaluation — what is well-established vs uncertain\n"
                "  - Practical implications and recommended actions\n"
                "  - Key conclusions and takeaways\n\n"
                "Be analytical, not descriptive. Draw non-obvious insights. "
                "Structure output under clear headings."
            )
        ),
        HumanMessage(
            content=(
                f"Topic: {state['topic']}\n\n"
                f"Research Data:\n{state['research_data']}\n\n"
                "Perform a comprehensive critical analysis and provide structured insights, "
                "patterns, conclusions, and recommendations."
            )
        ),
    ]

    response = llm.invoke(messages)
    return {"analysis": response.content}
