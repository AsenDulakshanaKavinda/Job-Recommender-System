
from langgraph.graph import StateGraph, START, END
from langchain_core.messages import HumanMessage, BaseMessage, SystemMessage, ToolMessage

from typing import TypedDict, Annotated, Sequence
from operator import add as add_messages

from src.job_recommender.core.exceptions_config import ProjectException
from src.job_recommender.core.logger_config import logger as log
from src.job_recommender.agent.tools import build_tools
from src.job_recommender.agent.tool_prompts import system_prompt

class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]

def should_continue(state: AgentState):
    last_message = state['messages'][-1]
    return hasattr(last_message, "tool_calls") and len(last_message.tool_calls) > 0

def build_rag_agent(session_id: str):
    """"
    Build and return a compiled rag_agent for a specific session_id.
    The retriever in tools will be initialized with the same session namespace.
    """

    tools, tool_dict, llm = build_tools(session_id=session_id)

    def call_llm(state: AgentState) -> AgentState:
        messages = list(state['messages'])
        messages = [SystemMessage(content=system_prompt)]
        message = llm.invoke(messages)
        return {"messages": [message]}
    
    def take_action(state: AgentState) -> AgentState:
        tool_calls = state['messages'][-1].tool_calls
        results = []
        for t in tool_calls:
            if t['name'] not in tool_dict:
                result = f"Tool {t['name']} not found"
            else:
                args = t['args']
                # call tool using it's invoke API
                if 'query' in args:
                    result = tool_dict[t['name']].invoke(args.get('query'))
                else:
                    result = tool_dict[t['name']].invoke(args)
            results.append(
                ToolMessage(
                    tool_call_id = t['id'],
                    name = t['name'],
                    content = str(result)
                )
            )

        return {"messages": results}
    
    # create graph
    graph = StateGraph(AgentState)

    # add nodes
    graph.add_node("llm", call_llm)
    graph.add_node("retriever_agent", take_action)

    # add edges
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
    return graph.compile()





