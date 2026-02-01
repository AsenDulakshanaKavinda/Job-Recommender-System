from langchain_chroma import Chroma

from system.client import load_embedding_model

def create_vector_store():
    try:
        vector_store = Chroma(
            collection_name="example_collection",
            embedding_function=load_embedding_model(),
            persist_directory="./chroma_langchain_db",
        )
        return vector_store
    
    except Exception as e:
        print(str(e))
    