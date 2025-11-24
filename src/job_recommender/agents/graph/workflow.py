
from langgraph.graph import StateGraph, START, END

from src.job_recommender.agents.nodes.nodes import AgentState, call_llm, take_action, should_continue

graph = StateGraph(AgentState)
graph.add_node("llm", call_llm)
graph.add_node("retriever_agent", take_action)

graph.add_edge(START, "llm")
graph.add_conditional_edges(
    "llm",
    should_continue,
    {
        True: "retriever_agent",
        False: END
    }
)

graph.add_edge("retriever_agent", "llm")

rag_agent = graph.compile()


