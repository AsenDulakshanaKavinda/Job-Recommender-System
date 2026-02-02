from langchain_core.prompts import ChatPromptTemplate

SYSTEM_PROMPT = """
system prompt for the creating custom plan

"""

def load_create_custom_plan_prompt():
    try:
        CREATE_CUSTOM_PLAN_PROMPT = ChatPromptTemplate.from_messages([
            ("system", SYSTEM_PROMPT),
            ("human", "{cv_text}")
        ])
        return CREATE_CUSTOM_PLAN_PROMPT
    except Exception as e:
        print(str(e))