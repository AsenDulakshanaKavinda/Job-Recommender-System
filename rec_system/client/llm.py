from langchain_mistralai import ChatMistralAI
from rec_system.utils import llm_config, log, RecommendationSystem

def load_llm_model():
    try:
        llm = ChatMistralAI(
            model=llm_config['llm_model'],
            api_key=llm_config['api_key']
        )
        log.info("Loading LLM.")
        return llm
    except Exception as e:
        RecommendationSystem(
            e,
            context={
                "operation": "Loading LLM."
            }
        )
    

