from typing import TypedDict, List

# -- --
class KeywordSchema(TypedDict):
    skills: List[str]
    job_keywords: List[str]

# -- --
class SkillGapSchema(TypedDict):
    existing_skills: List[str]
    missing_skills: List[str]
    skill_gaps: List[str]

# -- --
class JobSchema(TypedDict):
    title: str
    publish_at: str
    location: str
    job_url: str

# -- --
class StateSchema(TypedDict):
    filepath: str
    content: str
    keywords: KeywordSchema
    summery: str
    skill_gap: SkillGapSchema
    road_map: str
    jobs: List[JobSchema]
    # messages: 