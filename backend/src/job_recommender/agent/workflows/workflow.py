from src.job_recommender.core.logger_config import logger as log
from src.job_recommender.core.exceptions_config import ProjectException


# -- nodes
from src.job_recommender.agent.nodes.custome_nodes import *


from langgraph.graph import StateGraph, START, END


def create_workflow():
    # create the grapg
    workflow = StateGraph(StateSchema)

    # add node
    workflow.add_node("read_resume", read_resume_node)
    workflow.add_node("create_summery", create_summery_node)
    workflow.add_node("extract_keyword", extract_keyword_node)
    workflow.add_node("fetch_job", fetch_job_node)

    workflow.add_node("skill_gap", skill_gap_node)
    workflow.add_node("road_map", road_map_node)

    # add edges
    workflow.add_edge(START, "read_resume")
    workflow.add_edge("read_resume", "create_summery")
    workflow.add_edge("read_resume", "extract_keyword")
    # workflow.add_edge("extract_keyword", "fetch_job")
    workflow.add_edge("read_resume", "skill_gap")

    workflow.add_edge("skill_gap", "road_map")
    # workflow.add_edge("fetch_job", END)
    workflow.add_edge("create_summery", END)
    workflow.add_edge("extract_keyword", END)
    workflow.add_edge("road_map", END)

    try:
        log.info("Creaing workflow...")
        app = workflow.compile()
        return app
    except Exception as e:
        ProjectException(
            e,
            context = {
                "operation": "workflow"
            }
        )

