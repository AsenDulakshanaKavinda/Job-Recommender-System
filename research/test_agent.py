from langgraph.graph import StateGraph, START, END
from dotenv import load_dotenv
from typing import TypedDict, Annotated, Sequence
from langchain_core.messages import BaseMessage, SystemMessage, HumanMessage, ToolMessage
from langchain_mistralai import ChatMistralAI
from langchain_core.tools import tool
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode

load_dotenv()
model = ChatMistralAI(model_name="mistral-medium-latest")

# global variable to share document content
document_content = ""

class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]

@tool
def update(content: str):
    """ updates the document with the provided content """
    global document_content
    document_content = content
    return f"Document has bee updated successfully, the current content is:\n {document_content}"


@tool
def save(filename: str) -> str:
    """
    save the current document to a text file and finish the process
    args:
        filename: name of the text file
    """

    global document_content
    if not filename.endswith(".txt"):
        filename = filename + ".txt"

    try:
        with open(filename, 'w') as file:
            file.write(document_content)

        print(f"document saved successfully as {filename}")
        return f"document saved successfully as {filename}"

    except Exception as e:
        print(f"Error saving document: {e}")
        return f"Error saving document: {e}"

tools = [update, save]
model = model.bind_tools(tools)

my_tools = ToolNode(tools)


system_prompt = SystemMessage(
    content="""
        You are an email drafter, a helpful writing assistant.
        You help the user update or modify documents.

        Rules:
        - If the user wants to update content, call the `update` tool with FULL new content.
        - If the user wants to save and finish, call the `save` tool.
        - Always show the current document after modification.

        The current document is: {document_content}
    """
)

def out_agent(state: AgentState) -> AgentState:
    all_messages = [system_prompt] + list(state["messages"])
    response = model.invoke(all_messages)
    return {"message": list(state["messages"]) + [response]}













