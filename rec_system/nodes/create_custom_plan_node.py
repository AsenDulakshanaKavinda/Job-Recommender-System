
from rec_system.utils import *
from rec_system.client import load_llm_model
from rec_system.prompts import load_create_custom_plan_prompt
from rec_system.schemas import GraphState

def create_custom_plan(graphState: GraphState) -> GraphState:
    llm = load_llm_model()
    if not llm:
        raise RuntimeError("Cannot load the llm")
    
    CREATE_CUSTOM_PLAN_PROMPT = load_create_custom_plan_prompt()
    
    try:
        response = llm.invoke(
            CREATE_CUSTOM_PLAN_PROMPT.from_messages(
                cv_text=graphState["cv_text"]
            )
        )
        return graphState
    except Exception as e:
        print(str(e))
    
