
from rec_system.client import load_llm_model
from rec_system.prompts import load_missing_skills_extractor_prompt
from rec_system.schemas import JobRecState, skill_extractor_parser
from rec_system.utils import log, RecommendationSystemError


def extract_skills(job_rec_state: JobRecState) -> JobRecState:
    """ 
    Extract skills and missing skills from the cv

    args:
        job_rec_state ( JobRecState ) - the graph state
    return:
        job_rec_state: (JobRecState) - updated version with skills and missing skills
    exception:
        RuntimeError: if cannot load the llm
        ValueError: if cannot load the EXTRACT_SKILLS_PROMPT
        RecommendationSystemError: for any other error
    """

    llm = load_llm_model()
    if not llm:
        raise RuntimeError("Cannot load the llm in missing skill node.")
    
    EXTRACT_SKILLS_PROMPT = load_missing_skills_extractor_prompt()
    if not EXTRACT_SKILLS_PROMPT:
        log.error("Skill extractor prompt is missing.")
        raise ValueError("Skill extractor prompt is missing.")

    chain = EXTRACT_SKILLS_PROMPT | llm | skill_extractor_parser
    
    try:
        response = llm.invoke({
            "cv_content": job_rec_state["raw_cv_content"],
            "job_matches": job_rec_state["job_matches"]
        })
        job_rec_state["extracted_skills"] = "something" # TODO: add real values for the response
        job_rec_state["missing_skills"]= "something"
        return job_rec_state
    except Exception as e:
        RecommendationSystemError(
            e,
            context={
                "operation": "Extract skills Node"
            }
        )
    
