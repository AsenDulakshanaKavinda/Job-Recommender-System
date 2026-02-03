
from langchain_core.output_parsers import PydanticOutputParser

from .schemas import SummarizerOutput, SkillExtractorOutput

summarizer_parser = PydanticOutputParser(pydantic_object=SummarizerOutput)
skill_extractor_parser = PydanticOutputParser(pydantic_object=SkillExtractorOutput)







