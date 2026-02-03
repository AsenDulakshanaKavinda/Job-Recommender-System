
from rec_system.utils import *
from rec_system.client import load_llm_model
from rec_system.prompts import load_create_custom_plan_prompt
from rec_system.schemas import JobRecState, custom_plan_parser


from rec_system.utils import log, RecommendationSystemError

def create_custom_plan(job_rec_state: JobRecState) -> JobRecState:
    llm = load_llm_model()
    if not llm:
        raise RuntimeError("Cannot load the llm")
    
    CREATE_CUSTOM_PLAN_PROMPT = load_create_custom_plan_prompt()
    if not CREATE_CUSTOM_PLAN_PROMPT:
        log.error("Custom plan prompt missing")
        raise ValueError("Custom plan prompt missing")
    
    chain = CREATE_CUSTOM_PLAN_PROMPT | llm | custom_plan_parser
    
    try:
        response = llm.invoke(
            CREATE_CUSTOM_PLAN_PROMPT.from_messages(
                cv_text=job_rec_state["cv_text"]
            )
        )
        return job_rec_state
    except Exception as e:
        print(str(e))
    
