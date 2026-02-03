from langchain_core.prompts import ChatPromptTemplate
from rec_system.schemas import skill_extractor_parser
from rec_system.utils import log, RecommendationSystemError

SYSTEM_PROMPT = """
You are an information extraction system.

Extract structured information from the CV.

Identify:
1. Technical skills
2. Tools & frameworks
3. Soft skills (only if explicitly mentioned)
4. Identify the skills that user missing for the specific job roles

Rules:
- Do NOT infer skills not clearly present.
- Normalize skill names
- Avoid duplicates.

"""

def load_skills_extractor_prompt():
    try:
        format_instructions = skill_extractor_parser.get_format_instructions()
        if not format_instructions:
            log.error("Cannot create format instruction for the skill extractor prompt.")
            raise ValueError("format instruction error")
        EXTRACT_MISSING_SKILLS_PROMPT = ChatPromptTemplate.from_messages([
            ("system", SYSTEM_PROMPT),
            ("human", "cv content\n{cv_text}job roles{job_matches}\n\n{format_instructions}")
        ])
        return EXTRACT_MISSING_SKILLS_PROMPT
    except Exception as e:
        RecommendationSystemError(
            e, 
            context={
                "operation": "Loading skill extractor prompt."
            }
        )