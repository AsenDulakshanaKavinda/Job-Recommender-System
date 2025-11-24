
from pydantic import BaseModel, Field
from typing import Optional, Tuple

from langchain_core.tools import tool

from src.job_recommender.agent.tool_prompts import resume_summary_prompt, missing_skills_prompt, rode_map_prompt, extract_keyword_prompt

from src.job_recommender.vector_db.langchain_vector_db_manager import LangchainVectorDBManager
from src.job_recommender.core.model_config import ModelConfig
from src.job_recommender.core.exceptions_config import ProjectException
from src.job_recommender.core.logger_config import logger as log

# module-level placeholders used by the tool functions define below
retriever = None
model = None

@tool
def retriever_tool(query: str) -> str:
    """ This tool seach and return informantion from the vectorstore. """
    
    docs = retriever.invoke(query)

    if not docs:
        log.error("No relavent information found in the document.")
        return "No relavent information found in the document."
    
    try:
        results = []
        for i, doc in enumerate(docs):
            results.append(f"Source {i+1}: \n{doc.page_content}\n")
            log.info("Retrieving is complited.")
            return "\n".join(results)
    except Exception as e:
        log.error("Error while initiating `retriever_tool`")  
        ProjectException(
            e,
            context = {
                "operation": "retriever_tool",
                "value": ""
            },
            reraise=True
        )


@tool
def generate_resume_summary_tool(query: str) -> str:
    """ Generates ATS-optimized resume summaries. """

    docs = retriever_tool.invoke(query)

    if not docs:
        return "No relavent information found for summerization."
    
    try:
        resume_content = "\n\n".join([doc.page_content for doc in docs])
        chain = resume_summary_prompt | model
        resume_summery = chain.invoke({"resume_content": resume_content}).content
        return resume_summery
    except Exception as e:
        log.error("Error while initiating `generate_resume_summary_tool`")  
        ProjectException(
            e,
            context = {
                "operation": "retriever_tool",
                "value": ""
            },
            reraise=True
        )


@tool
def generate_missing_skills_tool(query: str):
    """ Analyzes resumes for skill gaps, weak areas, missing tools/technologies. """

    docs = retriever_tool.invoke(query)

    if not docs:
        return "No relavent information found for skill gaps."
    try:
        resume_content = "\n\n".join([doc.page_content for doc in docs])
        chain = missing_skills_prompt | model
        skill_gaph = chain.invoke({"resume_content": resume_content}).content
        return skill_gaph
    except Exception as e:
        log.error("Error while initiating `generate_missing_skills_tool`")  
        ProjectException(
            e,
            context = {
                "operation": "generate_missing_skills_tool",
                "value": ""
            },
            reraise=True
        )


@tool
def generate_road_map_tool(query: str):
    """ create a professional growth roadmap and future-skill plan based on the candidate’s background."""

    docs = retriever_tool.invoke(query)

    if not docs:
        return "No relavent information found to build rode-map."
    
    try:
        resume_content = "\n\n".join([doc.page_content for doc in docs])
        chain = rode_map_prompt | model
        rode_map = chain.invoke({"resume_content": resume_content}).content
        return rode_map
    except Exception as e:
        log.error("Error while initiating `generate_road_map_tool`")  
        ProjectException(
            e,
            context = {
                "operation": "generate_road_map_tool",
                "value": ""
            },
            reraise=True
        )


@tool
def extract_job_keywords_tool(query: str):
    """ extract job-related keywords from the content provided """

    docs = retriever_tool.invoke(query)

    if not docs:
        return "No relavent information found to extract job keywords."
    try:
        resume_content = "\n\n".join([doc.page_content for doc in docs])
        chain = extract_keyword_prompt | model
        job_keywords = chain.invoke({"resume_content": resume_content}).content
        return job_keywords
    except Exception as e:
        log.error("Error while initiating `extract_job_keywords_tool`")  
        ProjectException(
            e,
            context = {
                "operation": "extract_job_keywords_tool",
                "value": ""
            },
            reraise=True
        )

def build_tools(session_id: Optional[str] = None) -> Tuple[list, dict, object]:
    """
    Initialize a LangchainVectorDBManager with session_id, create retriever,
    Load LLM and bind tools.

    Args
        session_id: str

    Return
        tools, tool_dict, bound_llm: Tuple[list, dict, object]
    """

    global retriever, model

    # initializine vectorstore managet for this session
    vs_manager = LangchainVectorDBManager(session_id=session_id)
    retriever = vs_manager.as_retriever()

    # load models
    model_config = ModelConfig()
    model = model_config.llm_model_loader()

    # tools
    tools = [retriever_tool ,generate_resume_summary_tool, generate_missing_skills_tool, 
         generate_road_map_tool, extract_job_keywords_tool]
    
    tool_dict = {t.name: t for t in tools}

    # bined the tools to the LLM for use in agent loops
    bound_llm = model.bind_tools(tools)

    
    return tools, tool_dict, bound_llm




