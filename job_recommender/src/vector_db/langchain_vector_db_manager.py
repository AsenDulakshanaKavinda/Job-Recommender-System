import uuid
from datetime import datetime
from typing import Optional, List

from pinecone import Pinecone, ServerlessSpec

from langchain_pinecone import PineconeVectorStore

from job_recommender.src.core.api_key_config import api_key_config
from job_recommender.src.core.model_config import model_config

from job_recommender.src.core.logger_config import logger as log 
from job_recommender.src.core.exceptions_config import ProjectException

def generate_session_id() -> str:
    """"
    generate a unique session ID based on the current timestamp
    and random 8-character uuid format
    eg:-
        session_20250115_153045_a1b2c3d4
    """
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    unique_id = uuid.uuid4().hex[:8]
    return f"session_{timestamp}_{unique_id}"

class LangchainVectorDBManager:
    """
    wrapper class for manageing pinecone vector index connections and Langchain's PineconeVectorStore
    each instance operates within its own namespace (session_id) allowing isolated storage and retrieval of embeddings for a session/use

    """
    def __init__(self, session_id: Optional[str] = None):
        # pinecone index name
        self.index_name = "job-recommender-system"

        # genetate a new session id if none provided
        self.session_id = session_id or generate_session_id()

        # initialize pinecone client with api key
        self.pc = Pinecone(api_key=self._load_pinecone_api_key())

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

        # connect to the index
        self.index = self.pc.Index(self.index_name)   

        # create a langchain vector store wrapper, each session use its own namespace to avoid collisions
        self.vectorstore = PineconeVectorStore(
            index = self.index,
            embedding = embeddings,
            namespace = self.session_id,
            text_key = "text"
        )

    
    def upsert(self, text_chunks: List[str]):
        """
        Inster text chunks into the vector store

        - embed each text chunks into the vector store
        - store it under the session namespace
        - attach metadata including its source/session
        """
        self.vectorstore.add_texts(
            texts = text_chunks,
            metadatas = [{"source": self.session_id} for _ in text_chunks],
            # namespace = self.session_id
        )

    def as_retriever(self, **kwargs):
        """
        return the langchain retriever interface for semantic search
        pass parameters can pass via kwargs
        """
        return self.vectorstore.as_retriever(search_kwargs = kwargs)

    def delete(self):
        """
        delete all vectors in a session
        by filtering bases on the stored 'source' metadata.
        """
        self.pc.Index(self.index_name).delete(namespace=self.session_id, filter={"source": self.session_id})

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
                    "message": "key not found"
                }
            )
        except Exception as e:
            log.error(f"PINECONE_API_KEY not found in config: {e}")
            raise ProjectException(
                e,
                context = {
                    "operation": "load pinecone API key",
                    "message": "Unexpected error while loading key"
                }
            )





