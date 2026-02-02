
from rec_system.utils import log, RecommendationSystem
from rec_system.client import load_llm_model
from rec_system.prompts import load_summarizer_prompt
from rec_system.schemas import JobRecState, summarizer_parser



def summarizer(job_rec_state: JobRecState) -> JobRecState:
    llm = load_llm_model()
    if not llm:
        raise RuntimeError("Cannot load the llm.")
    
    SUMMARIZER_PROMPT = load_summarizer_prompt()
    if not SUMMARIZER_PROMPT:
        log.error("Summarizing prompt is missing.")
        raise ValueError()
    
    chain = load_summarizer_prompt() | load_llm_model() | summarizer_parser
    
    try:
        response = chain.invoke({
            "cv_content": job_rec_state["raw_cv_content"],
            "format_instructions": summarizer_parser.get_format_instructions()
        })
        log.info("Summarizing completed.")
        job_rec_state["cv_summary"] = response #TODO: add only the content
        return job_rec_state
    except Exception as e:
        RecommendationSystem(
            e,
            context={
                "operation": "Summarizer Node"
            }
        )
    
