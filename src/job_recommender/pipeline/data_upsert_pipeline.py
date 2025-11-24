"""
data upsert pipeline:
    1. read data from the resume
    2. preprocess the data (clean and chunking)
    3. upsert data to pinecone index (to a namespace)
"""

from typing import List

from src.job_recommender.loaders.pdf_loader import PdfLoader
from src.job_recommender.preprocessing.preprocessor import Preprocessor
from src.job_recommender.vector_db.langchain_vector_db_manager import LangchainVectorDBManager

from src.job_recommender.core.exceptions_config import ProjectException
from src.job_recommender.core.logger_config import logger as log

class DataUpsert:
    def __init__(self, filepath, session_id):
        self.filepath = filepath
        self.session_id = session_id


    def upsert_pipeline(self):
        """" read -> preprocess -> upsert the resume data to vectorstore. """
        try:
            resume_data = self.read_data(self.filepath)
            preprocess_data = self.preprocess_data(resume_data)
            self.upsert_data(preprocess_data)
            log.info(f"Successfully upsert the data from:{self.filepath} to namespace:{self.session_id}.")
        except Exception as e:
            log.error(f"Error while trying to upsert data to the vectorstore.")
            ProjectException(
                e,
                context={
                    "operation": "data upsert pipeline"
                },
                reraise=False
            )


    def read_data(self, filepath: str) -> str:
        """ 
        read data from the given filepath

        Args
            filepath: str - resume filepath

        Return
            content of the resume: str

        """
        try:
            with open(filepath, 'rb' ) as file:
                pdf_loader = PdfLoader(file)
                log.info(f"Successfully read data from: {self.filepath}.")
                return pdf_loader.text_extractor()
        except Exception as e:
            log.error(f"Error while trying to extract data from the resume.")
            ProjectException(
                e,
                context={
                    "operation": "data upsert pipeline - read_data"
                },
                reraise=False
            )


    def preprocess_data(self, content: str) -> List[str]:
        """ 
        preprocess the data from the given content

        Args
            cotent: List[str] - content of the resume

        Return
            preprocess content: List[str]

        """
        try:
            preprocessor = Preprocessor(content=content)
            log.info(f"Successfully preprocess data from: {self.filepath}.")
            return preprocessor.preprocess()
        except Exception as e:
            log.error(f"Error while trying to preprocessing data from: {self.filepath}.")
            ProjectException(
                e,
                context={
                    "operation": "data upsert pipeline - preprocess data"
                },
                reraise=False
            )


    def upsert_data(self, preprocess_data: List[str]) -> None:
        """ 
        upsert the preprocess data to vectorestore namespace

        Args
            session_id: str - session_id
            preprocess_data: List[str] - preprocess data

        Return
            None
        """
        try:
            vs_manager = LangchainVectorDBManager(session_id=self.session_id)
            vs_manager.upsert(preprocess_data)
            log.info(f"Successfully upsert data to: {self.session_id}.")

        except Exception as e:
            log.error(f"Error while trying to upserting data from: {self.filepath}.")
            ProjectException(
                e,
                context={
                    "operation": "data upsert pipeline - upserting data"
                },
                reraise=False
            )
    

