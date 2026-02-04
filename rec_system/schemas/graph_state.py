from typing import TypedDict, List
from uuid import uuid4
from pathlib import Path
 
class JobRecState(TypedDict):
    session_id: str
    original_filepath: Path # 
    raw_cv_content: str # 
    cv_summary: str # 
    extracted_roles: List[str]
    extracted_skills: List[str] #
    missing_skills: List[str] #
    learning_plan: str
    optimized_cv: str
    job_matches: List[str] # 
    user_goal: str

