from pathlib import Path
from typing import List
from uuid import uuid4

from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma


from rec_system.client import load_embedding_model
from rec_system.vectorstore import create_vector_store
from rec_system.schemas import GraphState
from rec_system.utils import documents_config


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
        print(f"Reading document, {len(docs)} docs.")
        return docs
    except Exception as e:
        print(str(e))

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
        print(f"splitted into {len(chunks)} chunks.")
        return chunks
    except Exception as e:
        print(str(e))


def store_to_vec_db(chunks: List[Document]) -> None:
    """
    Store embedded chunks in vector db

    args:
        chunks (List[Document]) - list of splitted docs
    return:
        None
    """
    try:
        vector_store = create_vector_store()
        uuids = [str(uuid4()) for _ in range(len(chunks))]
        vector_store.add_documents(documents=chunks, ids=uuids)
    except Exception as e:
        print(str(e))

# Node - 1
def read_store_vec_db(graph_state: GraphState) -> GraphState:
    """ 
    Read and store data in a Vector DB

    """
    filepath = "sample_data/What-is-a-Heart-Attack.pdf"
    try:
        if not docs:
            raise ValueError("Documents are missing.")
        docs = read_document(filepath)
        chunks = split_docs(docs)
        store_to_vec_db(chunks)
    except Exception as e:
        print(str(e))
   

   