
import uuid
from datetime import datetime

from typing import Optional, List

from pinecone import Pinecone

from job_recommender.src.core.api_key_config import api_key_config
from job_recommender.src.core.model_config import model_config

from job_recommender.src.core.logger_config import logger as log 
from job_recommender.src.core.exceptions_config import ProjectException

def generate_session_id() -> str:
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    unique_id = uuid.uuid4().hex[:8]
    return f"session_{timestamp}_{unique_id}"


class VectorDBManager:
    def __init__(self, session_id: Optional[str] = None):
        self.index_name = "job-recommender-system"
        self.pc = Pinecone(api_key=self._load_api_key())
        self.index = self.pc.Index(self.index_name)
        self.session_id = session_id or generate_session_id()


    def _load_api_key(self) -> str:
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
        
    def _validate_index(self):
        state = False if not self.pc.has_index(self.index_name) else True
        return state

    def create_index(self):
        try:
            if not self._validate_index():
                self.pc.create_index_for_model(
                    name=self.index_name,
                    cloud="aws",
                    region="us-east-1",
                    embed={
                        "model": model_config.embedding_model_loader(),
                        "field_map":{"text": "chunk"}
                    }
                )

                log.info(f"{self.index_name} created.")
        except Exception as e:
            ProjectException(
                e,
                context = {
                    "operation": "create index (vector index)",
                    "message": "Unexpected error while creating vector index"
                }
            )


    def upsert(self, text_chunks: List[str]):
        """
        Adding new vector embeddings into the database. 
        if a vector with the same ID already exists, it is updated; 
        otherwise, it is inserted.
        """
        # this work becouse index was created with an integrated embedding model
        records_to_upsert = []
        for i, chunk in enumerate(text_chunks):
            records_to_upsert.append({
                "id": f"{self.session_id}_{i}",
                "text": chunk,
                "metadata": {"source": self.session_id}
            })

        # upsert the records (raw text)
        self.index.upsert(records=records_to_upsert)
        log.info(f"Upserted {len(records_to_upsert)} chunks for session: {self.session_id}")


    def fetch(self):
        """
        Retrieving a specific vector and its associated metadata using its unique session_id in metadata.
        """
        vectors = self.index.list(prefix=f"{self.session_id}_")
        return vectors

    def search(self, query: str, top_k: int = 10) -> List[dict]:
        """
        searching for vectors most similar to a given query vector.
        """
        response = self.index.query(
            query = query,
            filter = {"source": self.session_id},
            top_k = top_k,
            include_metadata=True
        )
        return response.matches

    def delete(self):
        """
        Removing a specific vector and its metadata from the database.
        """
        self.index.delete(
            filter = {"source": {"$eq": self.session_id}}
        )
        
        
        



