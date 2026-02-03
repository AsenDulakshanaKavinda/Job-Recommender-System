
from langchain_mistralai import MistralAIEmbeddings

# from rec_system.utils import llm_config
from rec_system.utils import llm_config, log, RecommendationSystemError

def load_embedding_model():
    try:
        embedding_model = MistralAIEmbeddings(
            model=llm_config['embedding_model'],
            api_key=llm_config['api_key']
        )
        log.info("Embedding Loaded.")
        return embedding_model
    except Exception as e:
        RecommendationSystemError(
            e,
            context={
                "operation": "Loading embedding model."
            }
        )
    

