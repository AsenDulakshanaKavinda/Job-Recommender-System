from src.job_recommender.core.logger_config import logger as log
from src.job_recommender.core.exceptions_config import ProjectException


def import_extract_keyword_prompt(state_parameter):
    try:
        keyword_extract_prompt = f"""
            You are an expert resume analyst. Analyze the following resume content and extract the required information.

            Content: {state_parameter}

            Your tasks:
            1. Extract all skills mentioned (technical, soft skills, tools, technologies).
            2. Extract job-related keywords (roles, responsibilities, industry terms, domain-specific keywords).
            3. Do NOT add anything that is not present in the content.
            4. Return the answer in clean python list.
            """
        
        return keyword_extract_prompt
    except Exception as e:
        log.error(f"Unexpected error while importing keyword prompt: {e}")
        ProjectException(
            e,
            context = {
                "operation": "import_extract_keyword_prompt"
            },
            reraise = False
        )

def import_summery_prompt(state_parameter):
    try:
        summery_prompt = f"""
        You are an expert resume analyst. Analyze the following resume content and create a clear, concise professional summary.

        Content:
        {state_parameter}

        Your tasks:
        1. Produce a short paragraph (4–6 sentences) that summarizes the candidate’s:
        - background and experience
        - key strengths
        - technical and soft skills
        - major achievements (only if explicitly mentioned)
        2. Do NOT invent or assume information — only use details present in the content.
        3. Write in a professional tone suitable for a resume summary.
        4. Output only the summary paragraph, nothing else.
        """
        return summery_prompt
    except Exception as e:
        log.error(f"Unexpected error while importing skill gap prompt: {e}")
        ProjectException(
            e,
            context = {
                "operation": "import_skill_gap_prompt"
            },
            reraise = False
        )


def import_skill_gap_prompt(state_parameter):
    try:
        skill_gap_prompt = f"""
        You are an expert career analyst. Analyze the following resume content and identify skill gaps.

        Content:
        {state_parameter}

        Your tasks:
        1. Identify skills the candidate already has (technical, soft skills, tools, technologies).
        2. Identify missing or weak skills typically required for the candidate’s likely job roles.
        3. Compare the candidate’s skills against common industry expectations.
        4. Do NOT invent skills that are not mentioned.
        """
        return skill_gap_prompt
    except Exception as e:
        log.error(f"Unexpected error while importing skill gap prompt: {e}")
        ProjectException(
            e,
            context = {
                "operation": "import_skill_gap_prompt"
            },
            reraise = False
        )


def import_roadmap_prompt(state_parameter):
    try:
        roadmap_prompt = f"""
        You are a career coach and learning path designer. Based on the following skills the candidate is missing, create a simple and actionable roadmap.

        Missing Skills:
        {state_parameter}

        Your tasks:
        1. Create a clear step-by-step roadmap to help the candidate fill these skill gaps.
        2. Keep it simple and practical — assume the candidate is a beginner to intermediate learner.
        3. For each missing skill, include:
            - what to learn
            - recommended order
            - practical exercises or projects
        4. Present the roadmap as a clean numbered list.
        5. Do NOT add skills that are not in the missing_skills list.
        """
        return roadmap_prompt
    except Exception as e:
        log.error(f"Unexpected error while importing rodemap prompt: {e}")
        ProjectException(
            e,
            context = {
                "operation": "roadmap_prompt"
            },
            reraise = False
        )