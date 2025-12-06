
from src.job_recommender.core.model_config import model_config

from src.job_recommender.agent.states.state_schema import KeywordSchema, SkillGapSchema


from langchain.tools import tool
from langgraph.graph import StateGraph, START, END
from typing import List, TypedDict, Dict

class Client:
    def __init__(self):
        self.llm = model_config.llm_model_loader()

    def keyword_llm(self):
        return self.llm.with_structured_output(KeywordSchema)

    def skill_gap_llm(self):
        return self.llm.with_structured_output(SkillGapSchema)
    

client = Client()

