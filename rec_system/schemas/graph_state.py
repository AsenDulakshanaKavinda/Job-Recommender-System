from typing import TypedDict
from uuid import uuid4
from pathlib import Path
 
class JobRecState(TypedDict):
    session_id: str
    original_filepath: Path # 
    raw_cv_content: str # 
    cv_summary: str # 
    extracted_roles: list[str]
    extracted_skills: list[str] #
    missing_skills: list[str] #
    learning_plan: str
    optimized_cv: str
    job_matches: list[str] # 
    user_goal: str

