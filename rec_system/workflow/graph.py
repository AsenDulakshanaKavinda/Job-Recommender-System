from langgraph.graph import StateGraph, START, END
from rec_system.nodes import read_store_vec_db, summarizer, extract_skills, create_custom_plan
from rec_system.schemas import JobRecState


graph = StateGraph(JobRecState)

graph.add_node("read" , read_store_vec_db)
graph.add_node("summary", summarizer)
graph.add_node("extract_skills", extract_skills)
graph.add_node("create_custom_plan", create_custom_plan)


# graph.set_entry_point(START)
""" graph.add_edge("read", "summary")
graph.add_edge("summary", END) """

graph.add_edge(START, "read")
graph.add_edge("read", "summary")
graph.add_edge("summary", "extract_skills")
graph.add_edge("extract_skills", "create_custom_plan")
graph.add_edge("create_custom_plan", END)


app = graph.compile()





