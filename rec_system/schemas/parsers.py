
from langchain_core.output_parsers import PydanticOutputParser

from .schemas import SummarizerOutput

summarizer_parser = PydanticOutputParser(pydantic_object=SummarizerOutput)








