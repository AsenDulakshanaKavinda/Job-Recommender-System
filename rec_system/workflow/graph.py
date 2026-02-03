from langgraph.graph import StateGraph, START, END
from rec_system.nodes import read_store_vec_db
from rec_system.schemas import JobRecState


graph = StateGraph(StateGraph)

graph.add_node("read" , read_store_vec_db)

# graph.set_entry_point(START)
""" graph.add_edge("read", "summary")
graph.add_edge("summary", END) """

graph.add_edge(START, "read")
graph.add_edge("read", END)
# graph.add_edge("summary", END)

app = graph.compile()





