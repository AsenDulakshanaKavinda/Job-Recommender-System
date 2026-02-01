
from langchain_mistralai import MistralAIEmbeddings


def load_embedding_model():
    try:
        embedding_model = MistralAIEmbeddings(
            model="mistral-embed",
            api_key="enter api key"
        )
        return embedding_model
    except Exception as e:
        print(str(e))
    

