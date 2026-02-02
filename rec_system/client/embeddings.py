
from langchain_mistralai import MistralAIEmbeddings

# from rec_system.utils import llm_config
from rec_system.utils.handle_config import llm_config

def load_embedding_model():
    try:
        embedding_model = MistralAIEmbeddings(
            model=llm_config['embedding_model'],
            api_key=llm_config['api_key']
        )
        return embedding_model
    except Exception as e:
        print(str(e))
    

