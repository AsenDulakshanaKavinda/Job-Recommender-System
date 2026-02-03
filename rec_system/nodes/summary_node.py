
from rec_system.utils import log, RecommendationSystemError
from rec_system.client import load_llm_model
from rec_system.prompts import load_summarizer_prompt
from rec_system.schemas import JobRecState, summarizer_parser


def summarizer(job_rec_state: JobRecState) -> JobRecState:
    """ 
    create a summary of the cv

    args:
        job_rec_state ( JobRecState ) - the graph state
    return:
        job_rec_state: (JobRecState) - updated version with cv_summary
    exception:
        RuntimeError: if cannot load the llm
        ValueError: if cannot load the SUMMARIZER_PROMPT
        RecommendationSystemError: for any other error
    """

    llm = load_llm_model()
    if not llm:
        raise RuntimeError("Cannot load the llm.")
    
    SUMMARIZER_PROMPT = load_summarizer_prompt()
    if not SUMMARIZER_PROMPT:
        log.error("Summarizing prompt is missing.")
        raise ValueError("Summarizing prompt is missing.")
    
    chain = SUMMARIZER_PROMPT | llm | summarizer_parser
    
    try:
        response = chain.invoke({
            "cv_content": job_rec_state["raw_cv_content"],
            "format_instructions": summarizer_parser.get_format_instructions()
        })
        log.info("Summarizing completed.")
        # job_rec_state["cv_summary"] = response #TODO: add only the content
        # job_rec_state["job_matches"] = response
        return job_rec_state
    except Exception as e:
        RecommendationSystemError(
            e,
            context={
                "operation": "Summarizer Node"
            }
        )
    
