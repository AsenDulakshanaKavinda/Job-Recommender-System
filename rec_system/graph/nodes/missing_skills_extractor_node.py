
from rec_system.client import load_llm_model
from rec_system.prompts import load_missing_skills_extractor_prompt
from rec_system.schemas import GraphState

def extract_missing_skills(graphState: GraphState) -> GraphState:
    llm = load_llm_model()
    if not llm:
        raise RuntimeError("Cannot load the llm in missing skill node.")
    
    EXTRACT_MISSING_SKILLS_PROMPT = load_missing_skills_extractor_prompt()
    
    try:
        response = llm.invoke(
            EXTRACT_MISSING_SKILLS_PROMPT.from_messages(
                cv_text=graphState["cv_text"]
            )
        )
        return graphState
    except Exception as e:
        print(str(e))
    
