from langchain_core.prompts import ChatPromptTemplate

SYSTEM_PROMPT = """
You are a senior technical recruiter.
Summarize the following CV clearly and concisely.
Focus on:
- Core skills
- Experience
- Education
- Strengths

"""

def load_summarizer_prompt():
    try:
        SUMMARIZER_PROMPT = ChatPromptTemplate.from_messages([
            ("system", SYSTEM_PROMPT),
            ("human", "{cv_text}")
        ])
        return SUMMARIZER_PROMPT
    except Exception as e:
        print(str(e))