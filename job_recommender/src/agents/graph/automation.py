from langchain_core.messages import HumanMessage
from job_recommender.src.agents.graph.workflow import rag_agent

def automate():
    summery_query = "generate a summey of the entire resume PDF"
    summery_message = [HumanMessage(content=summery_query)]
    summery_result = rag_agent.invoke({'messages': summery_message})
    print("Generated summery: ")
    print(summery_result['messages'][-1].content)
    print("\n" + "-*" * 50 + "\n")

