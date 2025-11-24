"""
- simple Exception configurations for job recommender system.
"""

import sys
import traceback
from typing import Optional, Dict, Any
from .logger_config import logger

def format_error_message(error: Exception, tb) -> str:
    """
    create a detaild, readble error message.

    Args:
        error: The exception instrance
        tb: the traceback object.
    
    Return:
        formatted error message with file name, line number and error text.
    """
    if tb is None:
        exc_type, exc_val, exc_tb = sys.exc_info()
        tb = exc_tb

    if tb is None:
        return f"Error {str(error)} (no traceback available)."
    
    file_name = traceback.extract_tb(tb)[-1].filename
    line_number = traceback.extract_tb(tb)[-1].lineno
    full_trace = ''.join(traceback.format_tb(tb))

    return f"Error in [{file_name}] at line [{line_number}]: {str(error)} \nFull Traceback:\n{full_trace}"

class ProjectException(Exception):
    """
    Custom Exception class providing detailed, logged error information.
    """

    def __init__(
            self,
            error: Exception,
            *,
            context: Optional[Dict[str, Any]] = None,
            reraise: bool = True
    ):
        """
        Args:
            error: The Original exception.
            context: Optional extra information (user_id, job_id, api)
            reraise: If True, re-raise after logging (default: True)
        """

        exc_type, exc_val, exc_tb = sys.exc_info()
        self.context = context or {}

        # format message
        self.error_message = format_error_message(error, exc_tb)

        # include context in message for debugging
        if self.context:
            self.error_message += f" | Context: {self.context}"

        # log the error with full traceback
        logger.error(self.error_message, exc_info=True)

        # store original exception too
        self.original_exception = error

        super().__init__(self.error_message)

        if reraise:
            raise self

    def __str__(self):
        return self.error_message


if __name__ == "__main__":
    try:
        result = 10/0
    except Exception as e:
        ProjectException(
            e,
            context={"operation": "division_test", "value": 10}
        )
