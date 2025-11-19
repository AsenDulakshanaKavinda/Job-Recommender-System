import os
import sys
from typing import BinaryIO, List
import fitz

from langchain_core.document_loaders import PDF

from job_recommender.src.core.logger_config import logger as log 
from job_recommender.src.core.exceptions_config import ProjectException

class PdfLoader:
    def __init__(self):
        ...

    def text_extractor(self, uploaded_file: BinaryIO):
        """
        Extracts text from a PDF file-like object.

        Args:
            uploaded_file (BinaryIO): A readable file-like object (e.g., BytesIO or uploaded file stream).

        Returns:
            str: The extracted text from all pages.

        Raises:
            ProjectExceptions
        """


        try:
            with fitz.open(stream=uploaded_file.read(), filetype="pdf") as doc:
                if doc.page_count == 0:
                    log.warning("Empty PDF document")
                    return ""
                
                if self._ensure_size(uploaded_file) and self._ensure_readability(uploaded_file):
                    page_texts: List[str] = []
                    for page_num, page in enumerate(doc, start=1):
                        try:
                            page_text = page.get_text()
                            page_texts.append(page_text)
                            log.debug(f"Extracted text from page {page_num}")
                        except Exception as e:
                            log.error(f"Faild to extract text from {page_num}")
                            ProjectException(
                                e,
                                context = {
                                    "opetation": "text extractor page reader"
                                }
                            )
                
                    full_text = "\n".join(page_texts) # join once
                    log.info(f"Extracted text from { doc.page_count} pages, (total chars: {len(full_text)})")
                    return full_text
        except Exception as e:
            log.error(f"Unexpected error during PDF extraction")    
            ProjectException(
                e,
                context = {
                    "operation": "text extractor",
                    "message": "Failed to extract text from PDF"
                }
            )


    

    def _ensure_readability(self, uploaded_file: BinaryIO) -> bool:
        """ 
        Check the readabiity of the uploaded file, it should be a file-like object.

        args:
            uploaded file: BinaryIO - path of the uploaded file

        return:
            True - only if readable

        raise:
            ProjectException: if file not readable
        """


        if not hasattr(uploaded_file, 'read') or not callable(uploaded_file.read):
            log.warning("File not readable.")
            ProjectException(
                "Uploaded file must be a readable file-like object.",
                context={
                    "operation": "ensure readability of doc",
                }
            )
            return False
        else:
            log.info("File readable.")
            return True

    def _ensure_size(self, uploaded_file: BinaryIO) -> bool:
        """ 
        Check the size of the uploaded file,

        args:
            uploaded file: BinaryIO - path of the uploaded file

        return:
            True - only if it file size < 10MB

        raise:
            ProjectException: file size > 10MB
        """

        try:
            file_size = uploaded_file.seek(0, 2) # get the size
            uploaded_file.seek(0) # reset position
            if file_size > 10 * 1024 * 1024: # 10MB limit
                log.warning(f"File size {file_size}MB.")
                ProjectException(
                    "File too large, Maximum 10MB",
                    context = {
                        "operation": "check file size",
                        "limit": "10MB"
                    }
                )
                return False
            else:
                log.info(f"File size: {file_size}, under the limit.")
                return True
        except Exception as e:
            ProjectException(
                e,
                context = {
                    "operation": "check file size"
                }
            )


        





