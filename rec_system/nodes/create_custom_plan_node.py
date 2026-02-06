from rec_system.schemas import JobRecState
import os

from langchain_groq import ChatGroq
from langchain_mistralai import ChatMistralAI
from langchain.agents import create_agent
from langchain.agents.structured_output import ToolStrategy
from langchain_core.messages import AIMessage

from pydantic import BaseModel

from rec_system.prompts import load_create_custom_plan_prompt
from rec_system.tools import find_online_courses

from rec_system.utils import log, RecommendationSystemError

os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

class PlanOutput(BaseModel):
    plan: str

model_mistral = ChatMistralAI(
    model="mistral-large-latest",
    temperature=0.2,
)

model = ChatGroq(
    model="openai/gpt-oss-120b"
)


def create_custom_plan(job_rec_state: JobRecState) -> JobRecState:
    # Format the prompt with the actual values from job_rec_state
    prompt = load_create_custom_plan_prompt().format(
        raw_cv_content=job_rec_state["raw_cv_content"],
        missing_skills=job_rec_state["missing_skills"] 
    )

    agent = create_agent(
        model=model,
        tools=[find_online_courses],
        system_prompt=prompt,
        # response_format=ToolStrategy(PlanOutput)
    )
    
    try:
        result = agent.invoke({
            "raw_cv_content": job_rec_state["raw_cv_content"],
            "missing_skills": job_rec_state["missing_skills"],
        })

        final_ai_message = next(
            msg for msg in reversed(result["messages"])
            if isinstance(msg, AIMessage)
        )


        # final_message = result["messages"][-1]
        # print(final_message.content)

        job_rec_state["learning_plan"] = final_ai_message.content

        return job_rec_state
    
    except Exception as e:
        RecommendationSystemError(
            e,
            context={"operation": "create custom learning plan"}
        )




