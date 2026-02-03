from langchain_core.prompts import ChatPromptTemplate
from rec_system.schemas import summarizer_parser
from rec_system.utils import log, RecommendationSystemError

SYSTEM_PROMPT = """
You are an expert technical recruiter.

Summarize the candidate’s CV in a concise professional profile.
Focus on:
- Core background
- Years of experience (if inferable)
- Primary technical domains
- Career direction

Rules:
- No bullet points longer than one line.
- Do NOT invent experience.
- Use neutral, recruiter-friendly language.

Output a single paragraph summary.


"""

def load_summarizer_prompt():
    try:
        format_instructions = summarizer_parser.get_format_instructions()
        if not format_instructions:
            log.error("Cannot create format instruction for the summarizer prompt.")
            raise ValueError("format instruction error")

        SUMMARIZER_PROMPT = ChatPromptTemplate.from_messages([
            ("system", SYSTEM_PROMPT),
            ("human", "cv content\n{cv_text}\n\n{format_instructions}")
        ])
        return SUMMARIZER_PROMPT
    except Exception as e:
        RecommendationSystemError(
            e,
            context={
                "operation": "Loading summarizer prompt"
            }
        )