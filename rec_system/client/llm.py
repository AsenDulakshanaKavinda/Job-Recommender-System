from langchain_mistralai import ChatMistralAI

# from rec_system.utils import llm_config
from rec_system.utils.handle_config import llm_config

def load_llm_model():
    try:
        llm = ChatMistralAI(
            model=llm_config['llm_model'],
            api_key=llm_config['api_key']
        )
        return llm
    except Exception as e:
        print(str(e))
    

