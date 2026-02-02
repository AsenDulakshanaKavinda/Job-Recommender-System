

from rec_system.utils import *
from rec_system.client import load_llm_model
from rec_system.prompts import load_summarizer_prompt
from rec_system.schemas import GraphState

def summarizer(graphState: GraphState) -> GraphState:
    llm = load_llm_model()
    if not llm:
        raise RuntimeError("Cannot load the llm")
    
    SUMMARIZER_PROMPT = load_summarizer_prompt()
    
    try:
        response = llm.invoke(
            SUMMARIZER_PROMPT.from_messages(
                cv_text=graphState["cv_text"]
            )
        )
        return graphState
    except Exception as e:
        print(str(e))
    
