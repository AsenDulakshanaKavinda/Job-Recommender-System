
from pydantic import BaseModel, field_validator, Field
from typing import Optional, Dict

class LoggingConfig(BaseModel):
    level: str = "INFO"
    # filepath: str
    
    @field_validator("level")
    def validate_level(cls, v):
        validate_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        if v not in validate_levels:
            raise ValueError(f"Invalid logging level: {v}")
        return v
    
class AppConfig(BaseModel):
    name: str
    version: str

class LLMConfig(BaseModel):
    provider: str
    model_name: str
    temperature: float = Field(..., ge=0, le=1) # temperature must be in [0, 1]

class EmbeddingModelConfig(BaseModel):
    provider: str
    model_name: str

class Settings(BaseModel):
    logging: LoggingConfig
    app: AppConfig
    llm: Dict[str, LLMConfig]
    embedding_model: Dict[str, EmbeddingModelConfig]


