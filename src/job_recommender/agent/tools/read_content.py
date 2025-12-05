

from langchain_community.document_loaders import PyMuPDFLoader


from src.job_recommender.core.pdf_loader import PdfLoader
from src.job_recommender.core.preprocessor import Preprocessor

from src.job_recommender.core.logger_config import logger as log
from src.job_recommender.core.exceptions_config import ProjectException

from pathlib import Path


def read_content(filepath: Path) -> str:
    if not filepath:
        log.error("Resume file path is empty")
        ProjectException(
            "Resume filepath can't be empty!!!",
            context = {
                "operation": "read_content"
            }
        )

    try:
        with open(filepath, "+rb") as file:
            resume_loader = PdfLoader(file)
            raw_content = resume_loader.text_extractor()
            log.info("Extreacted raw data from pdf")

            preprocesser = Preprocessor(raw_content)
            cleaned_content = preprocesser.preprocess()
            log.info("Clened extreacted raw data from pdf")

            print(cleaned_content)

            return cleaned_content

    except Exception as e:
        ProjectException(
            e,
            context = {
                "operation": "read_content"
            }
        )

