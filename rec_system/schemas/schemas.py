from pydantic import BaseModel, Field, List

class SummarizerOutput(BaseModel):
    result: str = Field(description="The summarize result of the cv")

class SkillExtractorOutput(BaseModel):
    missing_skills: List[str] = Field(description="List of missing skills to")
    extracted_skills: List[str] = Field(description="List of skills user already have")