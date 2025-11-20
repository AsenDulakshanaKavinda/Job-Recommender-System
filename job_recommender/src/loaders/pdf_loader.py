import os
import sys
from typing import BinaryIO, List
import fitz



from job_recommender.src.core.logger_config import logger as log 
from job_recommender.src.core.exceptions_config import ProjectException

class PdfLoader:
    def __init__(self, uploaded_file: BinaryIO):
        self.uploaded_file = uploaded_file
        self._ensure_size()
        self._ensure_readability()
        

    def text_extractor(self) -> str:
        """
        Extracts text from a PDF file-like object.

        Args:
            self.uploaded_file (BinaryIO): A readable file-like object (e.g., BytesIO or uploaded file stream).

        Returns:
            str: The extracted text from all pages.

        Raises:
            ProjectException: If extraction fails or input in invalid.
        """


        try:
            pdf_content = self.uploaded_file.read()
            with fitz.open(stream=pdf_content, filetype="pdf") as doc:
                if doc.page_count == 0:
                    log.warning("Empty PDF document")
                    return ""
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
                                "opetation": "text extractor page reader",
                                "page number": page_num
                            }
                        )
                
                full_text = "\n".join(page_texts) # join once
                log.info(f"Extracted text from { doc.page_count} pages, (total chars: {len(full_text)})")
                return full_text
            
        except fitz.FileDataError as e:
            log.error("Invalid or corrupted PDF file")
            ProjectException(
                e,
                context={
                    "operation": "text extractor",
                    "message": "Invalid PDF file"
                }
            )
                    
        except Exception as e:
            log.error(f"Unexpected error during PDF extraction")    
            ProjectException(
                e,
                context = {
                    "operation": "text extractor",
                    "message": "Failed to extract text from PDF"
                }
            )


    

    def _ensure_readability(self) -> bool:
        """ 
        Check the readabiity of the uploaded file, it should be a file-like object.

        args:
            uploaded file: BinaryIO - path of the uploaded file

        return:
            True - only if readable

        raise:
            ProjectException: if file not readable
        """


        if not hasattr(self.uploaded_file, 'read') or not callable(self.uploaded_file.read):
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

    def _ensure_size(self) -> bool:
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
            original_pos = self.uploaded_file.tell() # save current position
            self.uploaded_file.seek(0, 2)
            file_size = self.uploaded_file.tell() # get the size
            self.uploaded_file.seek(original_pos) # reset position
            if file_size > 10 * 1024 * 1024: # 10MB limit
                log.warning(f"File size {file_size / (1024 * 1024):.2f}MB.")
                ProjectException(
                    "File too large, Maximum 10MB",
                    context = {
                        "operation": "check file size",
                        "limit": "10MB"
                    }
                )
                return False
            else:
                log.info(f"File size: {file_size / (1024 * 1024):.2f}MB, under the limit.")
                return True
        except Exception as e:
            ProjectException(
                e,
                context = {
                    "operation": "check file size"
                }
            )


        





