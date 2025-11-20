
import re

from typing import List

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from job_recommender.src.core.logger_config import logger as log 
from job_recommender.src.core.exceptions_config import ProjectException

class Preprocessor:
    def __init__(self, content: str):
        self.content = content

    def preprocess(self) -> List[str]:
        """
        clean and split the content

        return:
            list of clean and splitted content: List[str]
        """
        try:
            cleaned_content = self._clean_resume_text(self.content)
            splitted_content = self._splliter(cleaned_content)
            log.info(f"Content preprocessing completed")
            return splitted_content
        except Exception as e:
            ProjectException(
                e,
                context = {
                    "operation": "text preprocessing.",
                    "message": "Unexpected error while preprocessing text."
                }
            )


    def _splliter(self, cleaned_content: str, chunk_size: int = 300, chunk_overlap: int = 50) -> List[str]:
        """ 
        Split the cleaned text to chunks. 
        args:
            cleaned_text : str
            chunk_size : int
            chunk_overlap : int
        
        return:
            list of chunks (List[str])

        """
        try:
            splitter = RecursiveCharacterTextSplitter(
                chunk_size = chunk_size,
                chunk_overlap = chunk_overlap
            )
            chunks = splitter.split_text(cleaned_content)
            log.info(f"{len(chunks)}, chunks are created.")
            return chunks
        except Exception as e:
            ProjectException(
                e,
                context = {
                    "operation": "text splitter(chunking).",
                    "message": "Unexpected error while splitting the cleaned text."
                }
            )


    def _clean_resume_text(self, content : str) -> str:
        """
        clean resume text for embedding by removing unwanted characters, PII, bullets, symbols,
        URLs, emails, phone numbers, extra whitespace, and converting to lowercase.
        
        args:
            content: str
        
        return:
            cleand text: str
        """
        

        if not content :
            log.error(f"Content is empty!!!")
            return ""
        
        try:
            # 1. remove HTML tags
            text = re.sub(r"<.*?>", " ", content)

            # 2. remove bullets, arrows, checkmarks, stars ...
            text = re.sub(r"[\u2022\u2023\u25E6\u2043\u2219→✔✓★►▪◦*•-]", " ", text) 

            # 3. remove numbered or letterded lists at start of lines
            text = re.sub(r"^\s*(\d+|[a-zA-Z])[\.\)]\s*", " ", text, flags=re.MULTILINE)

            # 4. remove urls and emails
            text = re.sub(r"\S+@\S+", " ", text)
            text = re.sub(r"http\S+|www\S+", " ", text)

            # 5. remove phone numbers
            text = re.sub(r"\+?\d[\d\s\-\(\)]{7,}\d", " ", text)

            # 6. remove ellipses or repeated punctuation
            text = re.sub(r"\.{2,}", " ", text)
            text = re.sub(r"[!\"#$%&'()*+,/:;<=>?@[\\]^_`{|}~]", " ", text)

            # 7. remove non-ASCII characters (emojis, fancy symbols)
            text = re.sub(r"[^\x00-\x7F]+", " ", text)

            # 8. normalize whitespace
            text = re.sub(r"\s+", " ", text)

            # 9. convert to lowercase
            text = text.lower().strip()

            log.info(f"Text cleaning completed ")
            return text
        except Exception as e:
            ProjectException(
                e,
                context = {
                    "operation": "text cleaning.",
                    "message": "Unexpected error while cleaning text."
                }
            )

