from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph
from typing import TypedDict

# ---------------- State ----------------
class AgentState(TypedDict):
    summary: str
    decision: str

# ---------------- LLM ----------------
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.1
)

# ---------------- Node ----------------
def analyze_sentiment(state: AgentState):
    prompt = f"""
    You are an investment analyst.

    Based on the news summary below,
    return ONLY one word:
    Buy, Sell, or Hold.

    Summary:
    {state["summary"]}
    """

    # ✅ CORRECT METHOD
    response = llm.invoke(prompt)

    state["decision"] = response.content.strip()
    return state

# ---------------- Graph ----------------
graph = StateGraph(AgentState)
graph.add_node("analyze", analyze_sentiment)
graph.set_entry_point("analyze")
graph.set_finish_point("analyze")

investment_graph = graph.compile()

# ---------------- Public API ----------------
def investment_agent(summary: str) -> str:
    result = investment_graph.invoke({"summary": summary})
    return result["decision"]
