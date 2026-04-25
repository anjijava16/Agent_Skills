"""Search Agent — gathers initial information on the topic."""

from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage

from ..state import AgentState

# Set MODEL to "gpt-5" or "gpt-4o" depending on your OpenAI access
MODEL = "gpt-4o"


def search_node(state: AgentState) -> dict:
    """Node 1 — Search the web/LLM knowledge for key facts about the topic."""
    print(f"  [search_agent] Searching for: {state['topic']}")

    llm = ChatOpenAI(model=MODEL, temperature=0.3)

    messages = [
        SystemMessage(
            content=(
                "You are an expert researcher with broad knowledge across all domains. "
                "When given a topic, search your knowledge to gather:\n"
                "  - Key facts, figures, and statistics\n"
                "  - Important concepts and definitions\n"
                "  - Major players, events, or components\n"
                "  - Current trends and recent developments\n"
                "  - Relevant subtopics to explore\n\n"
                "Present your findings clearly under labelled sections. "
                "Be factual, thorough, and cite specific details."
            )
        ),
        HumanMessage(
            content=f"Search and gather comprehensive information about: {state['topic']}"
        ),
    ]

    response = llm.invoke(messages)
    return {"search_results": response.content}
