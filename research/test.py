import os
from dotenv import load_dotenv
from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated, Sequence
from langchain_core.messages import HumanMessage, ToolMessage, BaseMessage, SystemMessage
from operator import add as add_messages
from langchain_mistralai import ChatMistralAI, MistralAIEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_core.tools import tool
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()
model = ChatMistralAI(model_name="mistral-medium-latest")
embedding = MistralAIEmbeddings(model="mistral-embed")

pdf_path = "test_file.pdf"

if not os.path.exists(pdf_path):
    raise FileNotFoundError(f"{pdf_path} not found.")
pdf_loader = PyPDFLoader(pdf_path)

try:
    pages = pdf_loader.load()
    print(f"Pdf has loaded, pages: {len(pages)}")
except Exception as e:
    print(f"an error while loading docs {e}")

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size = 1000,
    chunk_overlap = 200
)

chunks = text_splitter.split_documents(pages)
print(f"total number of chunks: {len(chunks)}")

collection_name = "test-document-store"

try:
    vectorstore = Chroma.from_documents(
        documents = chunks,
        embedding = embedding,
        collection_name = collection_name
    )
    print(f"vs created with collection name {collection_name}")
except Exception as e:
    print(f"error from creating vs: {e}")

retriever = vectorstore.as_retriever(
    search_type = "similarity",
    search_kwargs = {"k": 3}
)

@tool
def retriever_tool(query: str) -> str:
    """ this tool search and return information from the vectorstore """
    docs = retriever.invoke(query)
    if not docs:
        return "No relevant information found in the document."
    results = []
    for i, doc in enumerate(docs):
        results.append(f"source {i+1}:\n{doc.page_content}\n")
    return "\n".join(results)

@tool
def generate_summary(query: str = "Summarize the entire document") -> str:
    """Generate a concise summary of the document or a specific topic/query."""
    docs = retriever.invoke(query)
    if not docs:
        return "No relevant information found for summarization."
    context = "\n\n".join([doc.page_content for doc in docs])
    summary_prompt = ChatPromptTemplate.from_template(
        "Summarize the following document content concisely:\n\n{context}\n\nSummary:"
    )
    chain = summary_prompt | model
    summary = chain.invoke({"context": context}).content
    return summary

@tool
def generate_mcqs(query: str = "Generate MCQs from the entire document", num_questions: int = 10) -> str:
    """Generate multiple-choice questions (MCQs) based on the document or a specific topic/query."""
    docs = retriever.invoke(query)
    if not docs:
        return "No relevant information found for generating MCQs."
    context = "\n\n".join([doc.page_content for doc in docs])
    mcq_prompt = ChatPromptTemplate.from_template(
        "Based on the following content, generate exactly {num_questions} multiple-choice questions. "
        "Each question should have 4 options (A-D), one correct answer, and a brief explanation.\n\n"
        "Content: {context}\n\nMCQs:"
    )
    chain = mcq_prompt | model
    mcqs = chain.invoke({"context": context, "num_questions": num_questions}).content
    return mcqs

tools = [retriever_tool, generate_summary, generate_mcqs]
tool_dict = {t.name: t for t in tools}
llm = model.bind_tools(tools)

class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]

def should_continue(state: AgentState):
    last_message = state['messages'][-1]
    return hasattr(last_message, "tool_calls") and len(last_message.tool_calls) > 0

system_prompt = """
You are an intelligent AI assistant that answers questions, generates summaries, and creates MCQs based on the PDF document.
Use the retriever_tool for general info retrieval.
Use generate_summary for summarization requests.
Use generate_mcqs for MCQ generation requests.
Always base outputs on retrieved content.
"""

def call_llm(state: AgentState) -> AgentState:
    messages = list(state['messages'])
    messages = [SystemMessage(content=system_prompt)] + messages
    message = llm.invoke(messages)
    return {'messages': [message]}

def take_action(state: AgentState) -> AgentState:
    tool_calls = state['messages'][-1].tool_calls
    results = []
    for t in tool_calls:
        print(f"Executing tool: {t['name']} with args {t['args']}")
        if t['name'] not in tool_dict:
            result = f"Tool {t['name']} not found"
        else:
            # Handle different tools
            args = t['args']
            if t['name'] == 'generate_mcqs':
                result = tool_dict[t['name']].invoke(args)
            else:
                result = tool_dict[t['name']].invoke(args.get('query', ''))
        print(f"Tool result: {result}")
        results.append(
            ToolMessage(
                tool_call_id = t['id'],
                name = t['name'],
                content = str(result)
            )
        )
    print("tools executed.")
    return {"messages": results}

graph = StateGraph(AgentState)
graph.add_node("llm", call_llm)
graph.add_node("retriever_agent", take_action)
graph.add_edge(START, 'llm')
graph.add_conditional_edges(
    'llm',
    should_continue,
    {
        True: 'retriever_agent',
        False: END
    }
)
graph.add_edge("retriever_agent", "llm")

rag_agent = graph.compile()

if __name__ == "__main__":
    # Automated run: Generate summary
    summary_query = "Generate a summary of the entire PDF document."
    summary_messages = [HumanMessage(content=summary_query)]
    summary_result = rag_agent.invoke({'messages': summary_messages})
    print("Generated Summary:")
    print(summary_result['messages'][-1].content)
    print("\n" + "-" * 50 + "\n")

    # Automated run: Generate 10 MCQs
    mcq_query = "Generate 10 MCQs from the entire PDF document."
    mcq_messages = [HumanMessage(content=mcq_query)]
    mcq_result = rag_agent.invoke({'messages': mcq_messages})
    print("Generated 10 MCQs:")
    print(mcq_result['messages'][-1].content)