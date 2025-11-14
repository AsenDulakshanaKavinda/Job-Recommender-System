
from pydantic import BaseModel, field_validator
from typing import Optional

class LoggingConfig(BaseModel):
    level: str = "INFO"
    # filepath: str
    
    @field_validator("level")
    def validate_level(cls, v):
        validate_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        if v not in validate_levels:
            raise ValueError(f"Invalid logging level: {v}")
        return v

class Settings(BaseModel):
    logging: LoggingConfig


