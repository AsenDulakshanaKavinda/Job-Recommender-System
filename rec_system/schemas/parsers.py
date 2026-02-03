
from langchain_core.output_parsers import PydanticOutputParser

from .schemas import SummarizerOutput, SkillExtractorOutput, CustomPlanOutput

summarizer_parser = PydanticOutputParser(pydantic_object=SummarizerOutput)
skill_extractor_parser = PydanticOutputParser(pydantic_object=SkillExtractorOutput)
custom_plan_parser = PydanticOutputParser(pydantic_object=CustomPlanOutput)






