"""
- simple logging configurations for job recommender system.
"""

import logging
import sys
import inspect
from functools import wraps
from typing import Any

def get_logger(name: str = "job_recommender_system") -> logging.Logger:
    """ Get a logger instance. """
    logger = logging.getLogger(name)

    if not logger.handlers:
        # set up basic logging
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)

    return logger


def log_api_call(api_name: str):
    """ simple decorator to log API calles. """
    def decorator(func):
        if inspect.iscoroutinefunction(func):
            @wraps(func)
            async def async_wrapper(*args, **kwargs):
                logger = get_logger()
                logger.debug(f"API call to: {api_name}")
                try:
                    result = await func(*args, **kwargs)
                    logger.debug(f"API call succeeded: {api_name}")
                    return result
                except Exception as e:
                    logger.error(f"API call to: {api_name} - {str(e)}", exc_info=True)
                    raise
            return async_wrapper
        else:
            @wraps(func)
            def sync_wrapper(*args, **kwargs):
                logger = get_logger()
                logger.debug(f"API call to: {api_name}")
                try:
                    result = func(*args, **kwargs)
                    logger.debug(f"API call succeeded: {api_name}")
                    return result
                except Exception as e:
                    logger.error(f"API call to: {api_name} - {str(e)}", exc_info=True)
                    raise
            return sync_wrapper
    return decorator
              
class LogContext:
    """ simple context manager for logging.  """
    def __init__(self, operation: str, **context):
        self.operation = operation
        self.context = context
        self.logger = get_logger()

    def __enter__(self):
        self.logger.debug(f"Starting {self.operation}")
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            self.logger.debug(f"Complited {self.operation}")
        else:
            self.logger.error(f"Faild {self.operation}: {exc_val}", exc_info=True)

# placeholder functions for compatability
def audit_log(event: str, **kwargs):
    logger = get_logger()
    logger.info(f"AUDIT: {event}")

def performance_log(operation: str, duration: float, **kwargs):
    logger = get_logger()
    logger.info(f"PERF: {operation} took {duration:.2f}s")
    
logger = get_logger()


