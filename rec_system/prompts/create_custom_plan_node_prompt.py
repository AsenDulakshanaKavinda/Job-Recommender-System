from langchain_core.prompts import ChatPromptTemplate
from rec_system.utils import log, RecommendationSystemError

SYSTEM_PROMPT = """
You are a senior technical mentor.

Create a practical learning plan to close the identified skill gaps.

Rules:
- Focus on applied learning, not theory.
- Use a 30–60–90 day structure.
- Use given tools to extract online course
- Use those courses as suggestions for users

Output in clear sections with bullet points with suggestions.
"""

def load_create_custom_plan_prompt():
    try:
        CREATE_CUSTOM_PLAN_PROMPT = ChatPromptTemplate.from_messages([
            ("system", SYSTEM_PROMPT),
            ("human", "cv content\n\n{cv_text}\ntarget job roles\n{target_job_roles}\nmissing skills\n{missing_skills}")
        ])
        return CREATE_CUSTOM_PLAN_PROMPT
    except Exception as e:
        RecommendationSystemError(
            e,
            context={
                "operation": "Create custom plan prompt"
            }
        )