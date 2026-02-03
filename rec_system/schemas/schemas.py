from pydantic import BaseModel, Field
from typing import List

class SummarizerOutput(BaseModel):
    cv_summary: str = Field(description="The summarize result of the cv")
    job_matches: str = Field(description="The job user can apply according to the cv")

class SkillExtractorOutput(BaseModel):
    missing_skills: List[str] = Field(description="List of missing skills to")
    extracted_skills: List[str] = Field(description="List of skills user already have")

class CustomPlanOutput(BaseModel):
    plan: str = Field(description="Custom plan created to learn and practice the missing skills")

 