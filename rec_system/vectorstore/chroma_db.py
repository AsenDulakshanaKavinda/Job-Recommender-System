from langchain_chroma import Chroma


from rec_system.client import load_embedding_model
from rec_system.utils import chromadb_config

class VectorStore:
    def __init__(self):
        self.collection_name = chromadb_config['collection_name']
        self.embedding_function = load_embedding_model()
        self.persist_directory = chromadb_config['persist_directory']
        self.vector_store = self._create_vector_store()

    def _create_vector_store(self):
        try:
            vector_store = Chroma(
                collection_name=self.collection_name,
                embedding_function=self.embedding_function,
                persist_directory=self.persist_directory,
            )
            return vector_store
        
        except Exception as e:
            print(str(e))


    def retriever(self, query: str):
        try:
            if not query:
                raise ValueError("Query cannot be empty.")
            return self.vector_store.similarity_search(
                query=query,
                k = chromadb_config['k']
            )
        except Exception as e:
            print(str(e))


