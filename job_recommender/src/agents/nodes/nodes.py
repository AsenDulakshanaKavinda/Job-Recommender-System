
from typing import TypedDict, Annotated, Sequence
from operator import add as add_messages
from langchain_core.messages import BaseMessage, SystemMessage, ToolMessage

from job_recommender.src.agents.prompts.tool_prompts import system_prompt
from job_recommender.src.agents.tools.tools import llm, tool_dict


class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]


def call_llm(state: AgentState) -> AgentState:
    """" call the llm """
    messages = list['messages']
    messages = [SystemMessage(content=system_prompt)] + messages
    message = llm.invoke(messages)
    return {'messages': [message]}


def take_action(state: AgentState) -> AgentState:
    """ use tools and output results """
    tool_calls = state['messages'][-1].tool_calls
    results = []
    for t in tool_calls:
        print(f"Executing tool: {t['name']} with args {t['args']}")
        if t['name'] not in tool_dict:
            result = f"Tool {t['name']} not found."
        else:
            # handle different tools
            args = t['args']
            result = tool_dict[t['name']].invoke(args)

        print(f"Tool result: {result}")
        results.append(
            ToolMessage(
                tool_call_id = t['id'],
                name = t['name'],
                content = str(result)
            )
        )
    print("tool executed.")
    return {"messages": results}


