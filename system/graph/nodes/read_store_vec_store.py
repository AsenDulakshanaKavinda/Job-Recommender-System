from pathlib import Path
from typing import List
from uuid import uuid4

from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma

from system.client import load_embedding_model
from system.vectorstore import create_vector_store

from system.schemas import GraphState



def read_document(filepath: Path) -> List[Document]:
    try:
        loader = PyPDFLoader(file_path=filepath)
        docs = loader.load()
        print(f"Reading document, {len(docs)} docs.")
        return docs
    except Exception as e:
        print(str(e))

def split_docs(docs: List[Document]) -> List[Document]:
    try:
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50
        )

        chunks = splitter.split_documents(docs)
        print(f"splitted into {len(chunks)} chunks.")
    except Exception as e:
        print(str(e))


def store_to_vec_db(chunks: List[Document]) -> None:
    try:
        vector_store = create_vector_store()
        uuids = [str(uuid4()) for _ in range(len(chunks))]
        vector_store.add_documents(documents=chunks, ids=uuids)
        return
    except Exception as e:
        print(str(e))


# def read_store_vec_db(graph_state: GraphState) -> GraphState:
def read_store_vec_db():
    filepath = "sample_data/What-is-a-Heart-Attack.pdf"
    docs = read_document(filepath)
    chunks = split_docs(docs)
    store_to_vec_db(chunks)
   