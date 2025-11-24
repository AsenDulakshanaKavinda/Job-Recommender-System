import os
import json

from dotenv import load_dotenv
from typing import List, Dict, Optional

from src.job_recommender.core.exceptions_config import ProjectException
from src.job_recommender.core.logger_config import logger as log

load_dotenv()

# todo - add `opentelemetry`
class ApiKeyConfig:
    """
    Utility class that loads and validates API keys needed across the application.

    Supports two loading strategies:
        1. JSON playload stored in env variables `apikeys`.
        2. Individual environment variables defined in `REQUIRED_KEYS`.

    Usage:
        config = ApiKeyConfig()
        keys = config.load() # returns dict of loaded keys 
    """

    REQUIRED_KEYS: List[str] = ["MISTRAL_API_KEY", "PINECONE_API_KEY"]

    def __init__(self, env_provider=os.getenv):
        """
        Args:
            env_provider (callable) : DI fro env varibale access (mock for tests).
        """
        self._env = env_provider
        
        # hoalds API keys after being loaded from env or json
        self._api_keys: Dict[str, Optional[str]] = {}


    def load(self) -> Dict[str, str]:
        """
        Load API keys using.

        Return:
            dict: a mapping of required API keys
        
        Raise:
            ProjectException: if any required key is missing or invalid
        """

        self._read_json_if_present()
        self._load_indicidual_keys()
        self._validate_keys()

        # freeze dict to avoid mutation after loading
        return dict(self._api_keys)
        

    def _read_json_if_present(self):
        """ Load keys via JSON-based env variable `apikeys`, if present. """

        raw = self._env("apikeys")
        if not raw:
            return
        
        try:
            parsed = json.loads(raw)
            if not isinstance(parsed, dict):
                raise ValueError("Environment variable 'apikey' must contain a JSON object.")
            
            log.info("Loaded API keys from JSON enviroment variable.")
            self._api_keys.update(parsed)
        except Exception as e:
            ProjectException(e, context={"operation": "parse json env 'apikeys"}, reraise=True)

    def _load_indicidual_keys(self):
        """ Load missing keys from individual environment keys"""
        for key in self.REQUIRED_KEYS:
            if key not in self._api_keys or not self._api_keys[key]:
                value = self._env(key)
                if value:
                    log.info(f"Loaded API key from environment variable: {key}")
                    self._api_keys[key] = value

    def _validate_keys(self):
        """ Ensure all the required keys are present an non-empty """
        missing = [key for key in self.REQUIRED_KEYS if not self._api_keys.get(key)]

        if missing:
            ProjectException (
                f"Missing API keys: {missing}", 
                context={
                    "operation": "validate required api keys", 
                    "value": missing
                },
                reraise=True
            )
        log.info(f"All the API keys are successfully validated.")



api_key_config = ApiKeyConfig()





