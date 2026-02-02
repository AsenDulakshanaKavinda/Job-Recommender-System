from langchain_core.prompts import ChatPromptTemplate

SYSTEM_PROMPT = """
system prompt for the missing skills

"""

def load_missing_skills_extractor_prompt():
    try:
        EXTRACT_MISSING_SKILLS_PROMPT = ChatPromptTemplate.from_messages([
            ("system", SYSTEM_PROMPT),
            ("human", "{cv_text}")
        ])
        return EXTRACT_MISSING_SKILLS_PROMPT
    except Exception as e:
        print(str(e))