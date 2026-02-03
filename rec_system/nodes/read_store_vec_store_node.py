from pathlib import Path
from typing import List
from uuid import uuid4

from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma


from rec_system.client import load_embedding_model
from rec_system.vectorstore import chromadb
from rec_system.schemas import JobRecState
from rec_system.utils import documents_config, log, RecommendationSystemError


def read_document(filepath: Path) -> List[Document]:
    """ 
    Read PDF documents in given filepath.
    
    args:
        filepath (Path) - filepath to the PDF document
    return
        docs (List[Document]) - list of docs
    """
    try:
        loader = PyPDFLoader(file_path=filepath)
        docs = loader.load()
        log.info(f"Reading document, loading: {len(docs)} docs.")
        return docs
    except Exception as e:
        RecommendationSystemError(
            e,
            context={
                "operation": "Reading document"
            }
        )

def split_docs(docs: List[Document]) -> List[Document]:
    """ 
    Split document using RecursiveCharacterTextSplitter.

    args:
        docs (List[Document]) - list of docs
    return:
        chunks (List[Document]) - list of splitted docs
    exceptions:

    """
    try:
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=documents_config['chunk_size'],
            chunk_overlap=documents_config['chunk_overlap']
        )
        chunks = splitter.split_documents(docs)
        log.info(f"splitted into chunk, {len(chunks)} chunks created..")
        return chunks
    except Exception as e:
        RecommendationSystemError(
            e,
            context={
                "operation": "Splitting documents"
            }
        )

def store_to_vec_db(chunks: List[Document]) -> None:
    """
    Store embedded chunks in vector db

    args:
        chunks (List[Document]) - list of splitted docs
    return:
        None
    """
    try:
        vector_store = chromadb.vector_store
        uuids = [str(uuid4()) for _ in range(len(chunks))]
        log.info("Storing info in vs")
        vector_store.add_documents(documents=chunks, ids=uuids)
    except Exception as e:
        RecommendationSystemError(
            e,
            context={
                "operation": "Store info into vs"
            }
        )
        
# Node - 1
def read_store_vec_db(job_rec_state: JobRecState) -> JobRecState:
    """ 
    Read and store data in a Vector DB
    """

    job_rec_state["original_filepath"] = "sample_data/What-is-a-Heart-Attack.pdf"
    try:
        if not job_rec_state["original_filepath"]:
            log.error("Filepath is missing.")
            raise ValueError("Filepath is missing.")
        
        docs = read_document(job_rec_state["original_filepath"])
        chunks = split_docs(docs)
        store_to_vec_db(chunks)
        log.info("Storing info in vs is Completed.")
        return job_rec_state
    except Exception as e:
        RecommendationSystemError(
            e, 
            context={
                "operation": "Reading and storing vs NODE"
            }
        )
   

   