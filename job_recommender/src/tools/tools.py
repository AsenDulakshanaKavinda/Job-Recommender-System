
from pydantic import BaseModel, Field

from langchain_core.tools import tool

from job_recommender.src.vector_db.langchain_vector_db_manager import LangchainVectorDBManager
from job_recommender.src.core.logger_config import logger as log 
from job_recommender.src.core.exceptions_config import ProjectException

class RetrieverInput(BaseModel):
    query: str = Field(description="the system prompt")

@tool
def retriever_tool(query: str) -> str:
    """ This tool seach and return informantion from the vectorstore. """
    
    vs_manager = LangchainVectorDBManager() # * session id wiil or will not need
    retriever = vs_manager.as_retriever({"k": 10})
    docs = retriever.invoke(query)

    if not docs:
        log.error("No relavent information found in the document.")
        return "No relavent information found in the document."
    
    try:
        results = []
        for i, doc in enumerate(docs):
            results.append(f"Source {i+1}: \n{doc.page_content}\n")
            log.info("Retrieving is complited.")
            return "\n".join(results)
    except Exception as e:
        log.error("Error while initiating `retriever_tool`")  
        raise ProjectException(
            e,
            context = {
                "operation": "retriever_tool"
            }
        )


@tool
def 












