import os
from dotenv import load_dotenv
from pydantic import BaseModel

from tenacity import retry, stop_after_attempt, wait_exponential

from langchain_mistralai import ChatMistralAI, MistralAIEmbeddings
from langchain_groq import ChatGroq

from src import Settings, api_key_config, project_config, log, log_api_call, ProjectException # todo - add log api calls to model and embedding loaders

class ModelSchema(BaseModel):
    llm: str
    embedding_model: str

class ModelConfig:
    def __init__(self):
        env = os.getenv("ENV", "dev").lower()

        if env != "production":
            load_dotenv()
            log.info("RUNNING IN LOCAL/DEV MODE: .env loaded.")
        else:
            log.info("RUNNING IN - PRODUCTION - MODE!!!: Using injected env vars.")

        self._api_key_config = api_key_config

        try:
            raw_config = project_config
            self._project_config = Settings(**raw_config.config).model_dump()
            print(self._project_config)
            log.info("YAML CONFIG LOADED AND VALIDATED.")
        except Exception as e:
            log.error(f"config validation error {e}")
            ProjectException(
                e,
                context = {
                    "operation" : "Model loader"
                }
            )

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    def llm_model_loader(self):
        """ 
        Load the LLM Model according to the configuration in config and env.
            args: None
            return : llm
        """
        llm_block = self._project_config.get("llm", {})
        provider_key = os.getenv("LLM_PROVIDER", "mistral")
        if provider_key not in llm_block:
            log.warning(f"LLM provider `{provider_key}` not found; falling back to `mistral`")
            provider_key = 'mistral'

        llm_config = llm_block[provider_key]
        provider = llm_config.get("provider")
        model_name = llm_config.get("model_name")
        temperature = llm_config.get("temperature", 0.2)
        log.info(f"Loading LLM: Provider={provider}, model={model_name}")

        if provider_key == "mistral":
            return ChatMistralAI(
                model_name=model_name,
                temperature=temperature
            )
        else:
            log.error(f"Unsupported LLM provider: {provider}")
            ProjectException(
                "Unsupported LLM provider",
                context={
                    "operation": "load llm model"
                }
            )

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    def embedding_model_loader(self):
        """ 
        Load the embedding Model according to the configuration in config and env.
            args: None
            return : embedding model
        """
        enbedding_block = self._project_config.get("embedding_model", {})
        provider_key = os.getenv("EMBEDDING_PROVIDER", "mistral")
        if provider_key not in enbedding_block:
            log.warning(f"Embedding provider `{provider_key}` not found; falling back to `mistral`")
            provider_key = 'mistral'

        llm_config = enbedding_block[provider_key]
        provider = llm_config.get("provider")
        model_name = llm_config.get("model_name")
        log.info(f"Loading Embedding: Provider={provider}, model={model_name}")

        if provider_key == "mistral":
            return MistralAIEmbeddings(
                model=model_name,
            )
        else:
            log.error(f"Unsupported Embedding provider: {provider}")
            ProjectException(
                "Unsupported Embedding provider",
                context={
                    "operation": "load embedding model"
                }
            )

model_config = ModelConfig()

# This decorator applies retry logic to the function it wraps.
# It uses the 'tenacity' library to handle transient failures automatically.
# - 'stop=stop_after_attempt(3)': Stops retrying after 3 total attempts (original call + 2 retries).
#   If all attempts fail, the last exception is raised.
# - 'wait=wait_exponential(multiplier=1, min=4, max=10)': Uses exponential backoff for wait times between retries.
#   Wait time calculation: min(max(multiplier * 2**(attempt-1), min), max) seconds.
#   Examples:
#     - 1st retry: min(max(1*1, 4), 10) = 4 seconds
#     - 2nd retry: min(max(1*2, 4), 10) = 4 seconds
#     - (If more: 3rd would be 4s, 4th 8s, 5th+ 10s)
# This makes the function resilient to temporary issues like network timeouts without manual error handling.