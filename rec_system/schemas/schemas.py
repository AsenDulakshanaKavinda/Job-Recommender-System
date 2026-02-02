from pydantic import BaseModel, Field

class SummarizerOutput(BaseModel):
    result: str = Field(description="The summarize result of the cv")