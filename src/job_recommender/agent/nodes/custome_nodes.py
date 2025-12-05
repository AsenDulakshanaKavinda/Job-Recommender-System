from typing import List


from src.job_recommender.core.logger_config import logger as log
from src.job_recommender.core.exceptions_config import ProjectException

# -- state
from src.job_recommender.agent.states.state_schema import StateSchema, JobSchema

# -- import prompts
from src.job_recommender.agent.prompts.node_prompts import import_extract_keyword_prompt, import_summery_prompt, import_skill_gap_prompt, import_roadmap_prompt

# -- import LLMs
from src.job_recommender.agent.LLM.client import client

# -- import tool
from src.job_recommender.agent.tools.fetch_jobs import fetch_jobs_from_linkedin
from src.job_recommender.agent.tools.read_content import read_content




# 1 - read resume - 
def read_resume_node(state: StateSchema) -> StateSchema:
    """ read and preprocess the resume data """
    content = read_content(state["filepath"]) 
    return {"content": content}

# 2 - extract job keywords - 
def extract_keyword_node(state: StateSchema) -> StateSchema:
    """ extract job related keyword and skill and return as a list."""

    try:
        log.info("Extracting keyword...")
        keywords = client.keyword_llm().invoke(import_extract_keyword_prompt(state_parameter={state['content']}))
        if not keywords:
            log.warning("Extracting keyword faild...")
        return {"keywords": keywords}
    except Exception as e:
        ProjectException(
            e,
            context = {
                "operation": "extract_keyword_node"
            }
        )


# 3 - create a summery - 
def create_summery_node(state: StateSchema) -> StateSchema:
    """ creating a summey of the content """

    try:
        log.info("Creating summery...")
        summery = client.llm.invoke(import_summery_prompt(state_parameter={state["content"]}))
        if not summery:
            log.warning("Extracting keyword faild...")
        return {"summery": summery}
    except Exception as e:
        ProjectException(
            e,
            context = {
                "operation": "create_summery_node"
            }
        )   


# 3 - skill gap - 
def skill_gap_node(state: StateSchema) -> StateSchema:
    """ find the skill gap and missing skills from the content accoring to jobs"""

    try:
        log.info("Creating skill gaps...")
        skill_gap = client.skill_gap_llm().invoke(import_skill_gap_prompt(state_parameter={state["content"]}))
        if not skill_gap:
            log.warning("Extracting skill_gap faild...")
        
        return {"skill_gap": skill_gap}
    except Exception as e:
        ProjectException(
            e,
            context = {
                "operation": "skill_gap_node"
            }
        )   



# 4 - create a rodemap - 
def road_map_node(state: StateSchema) -> StateSchema:
    """create a road map to learn the missing skills in the state """
    try:
        log.info("Creating  Road map...")
        road_map = client.llm.invoke(import_roadmap_prompt(state_parameter={'missing_skills': state["skill_gap"]["missing_skills"]}))
        if not road_map:
            log.warning("Genetating roadmap faild...")
        return {"road_map": road_map}
    except Exception as e:
        ProjectException(
            e,
            context = {
                "operation": "road_map_node"
            }
        ) 
   


# 5 - fetch jobs - 
def fetch_job_node(state: StateSchema) -> StateSchema:
    """ fetch jobs from LinkedIn using extracted job keyword. """
    
    job_keywords = state['keywords']['job_keywords']

    if not job_keywords:
        log.info("The job_keywords list is empty")
        ProjectException(
            "The job_keywords list cannot be empty.",
            context = {
                "operation": "fetch_job_node"
            }
        )
    

    # location
    location = "sri lanka"

    # call the tool
    raw_jobs = fetch_jobs_from_linkedin(["AI engineer"], location)
    if not raw_jobs:
        log.error("The job_keywords list is empty")
        ProjectException(
            "The job_keywords list cannot be empty.",
            context = {
                "operation": "fetch_job_node"
            }
        )


    parsed_jobs: List[JobSchema] = []
    try:
        for job in raw_jobs:
            parsed_jobs.append({
                "title": job.get("title", ""),
                "publish_at": job.get("publishDate", ""),
                "location": job.get("location", ""),
                "job_url": job.get("jobUrl", "")
            })
        print("parsed_jobs", parsed_jobs)

        return {"jobs": parsed_jobs}
    
    except Exception as e:
        log.error("Unexpected erroe while fettching jobs from LinkedIn")
        ProjectException(
            e,
            context = {
                "operation": "fetch_job_node"
            }
        )


