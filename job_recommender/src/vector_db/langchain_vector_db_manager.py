import uuid
from datetime import datetime
from typing import Optional, List

from pinecone import Pinecone, ServerlessSpec
from langchain_pinecone import PineconeVectorStore

from src import api_key_config, model_config, log, ProjectException, session_id




class LangchainVectorDBManager:
    """
    Wrapper class for manageing pinecone vector index connections and Langchain's PineconeVectorStore
    each instance operates within its own namespace (session_id) allowing isolated storage and retrieval of embeddings for a session/use

    """
    def __init__(self, session_id: Optional[str] = None):
        try:    
            # pinecone index name
            self.index_name = "job-recommender-system"

            # session id
            self.session_id = session_id

            # initialize pinecone client with api key
            self.pc = Pinecone(api_key=self._load_pinecone_api_key())
            log.info(f"Pinecone client initialized.")

            # load the embedding model
            embeddings = model_config.embedding_model_loader()

            # create a pinecone index if it doesn't already exist.
            if not self.pc.has_index(self.index_name):
                self.pc.create_index(
                    name = self.index_name,
                    dimension = 1536,
                    metric = "cosine",
                    spec = ServerlessSpec(cloud="aws", region="us-east-1"),
                )
            log.info(f"{self.index_name} wasn't availabel, new {self.index_name} created.")
        
            # connect to the index
            self.index = self.pc.Index(self.index_name) 
            log.info(f"Connected to the {self.index_name}.")

            # create a langchain vector store wrapper, each session use its own namespace to avoid collisions
            self.vectorstore = PineconeVectorStore(
                index = self.index,
                embedding = embeddings,
                namespace = self.session_id,
                text_key = "text"
            )
            log.info(f"Created langchain vector store name:{self.index}, namespace:{self.session_id}")
        except Exception as e:
            log.error(f"Error while initiate 'LangchainVectorDBManager'.")  
            ProjectException(
                e,
                context = {
                    "operation": f"initiating 'LangchainVectorDBManager'",
                    "value": "Failed to initiate the Index."
                },
                reraise=True

            )
    
    def upsert(self, text_chunks: List[str]):
        """
        Inster text chunks into the vector store

        - embed each text chunks into the vector store
        - store it under the session namespace
        - attach metadata including its source/session

        Args
            text_chunks: List[str] - preprocessed text chunks from the preprocessing.

        Raise:

        """
        try:
            self.vectorstore.add_texts(
                texts = text_chunks,
                metadatas = [{"source": self.session_id} for _ in text_chunks],
                namespace = self.session_id
            )
            log.info(f"Data successfully upserted to the index")
        except Exception as e:
            log.error(f"Error while upserting data into index.")
            ProjectException(
                e,
                context = {
                    "operation": "Upsert",
                    "value": "Faild to upsert."
                },
                reraise=True
            )

    def as_retriever(self, **kwargs):
        """
        return the langchain retriever interface for semantic search
        pass parameters can pass via kwargs
        """
        
        try:
            log.info(f"Retrieving data from index.")
            return self.vectorstore.as_retriever(search_kwargs = kwargs)
        except Exception as e:
            log.error(f"Error while retrieving data from index.")
            ProjectException(
                e,
                context = {
                    "operation": "as_retriever",
                    "value": "Faild to retrieve."
                },
                reraise=True
            )

    def delete(self):
        """
        delete all vectors in a session
        by filtering bases on the stored 'source' metadata.
        """
        
        try:
            log.info(f"Deleting index: {self.index_name}.")
            self.pc.Index(self.index_name).delete(namespace=self.session_id, filter={"source": self.session_id})
        except Exception as e:
            log.error(f"Error while deleting data from index.")
            ProjectException(
                e,
                context = {
                    "operation": "delete",
                    "value": "Faild to delete."
                },
                reraise=True
            )

    def _load_pinecone_api_key(self) -> str:
        """
        safely load the pinecone api key
        """
        try:
            keys = api_key_config.load()
            pinecone_key = keys["PINECONE_API_KEY"]
            return pinecone_key
        except KeyError:
            log.error("PINECONE_API_KEY not found in config.")
            raise ProjectException(
                ValueError("Missing PINECONE_API_KEY"),
                context={
                    "operation": "load pinecone API key",
                    "value": "key not found"
                }
            )
        except Exception as e:
            log.error(f"PINECONE_API_KEY not found in config: {e}")
            raise ProjectException(
                e,
                context = {
                    "operation": "load pinecone API key",
                    "value": "Unexpected error while loading key"
                }
            )


vs


