"""
Load application configuration based on the current environment.

Environment Variables:
- ENV: Defines the runtime environment (e.g., 'prod', 'dev').
- DEV_PROD_FILE: Path to the production configuration file.
- DEV_ENV_FILE: Path to the development configuration file.

Behavior:
- If ENV == 'prod', loads configuration from DEV_PROD_FILE.
- Otherwise, loads configuration from DEV_ENV_FILE.

Raises:
- RuntimeError: For unexpected failure during loading.
"""

import os
from configparser import ConfigParser
from dotenv import load_dotenv; load_dotenv()


def load_config():
    try:
        env = os.getenv("ENV", "").lower()

        config_file = os.getenv(
            "DEV_PROD_FILE" if env == "prod" else "DEV_ENV_FILE"
        )

        if not config_file:
            raise RuntimeError("Config file env variable missing")
        
        config = ConfigParser()
        config.read(config_file)
        return config
    except Exception as e:
        raise RuntimeError("Failed to load Configuration") from e


config = load_config()

llm_config = {
    "api_key" : os.getenv(config['LLM']['KEY']),
    'llm_model': config['LLM']['MODEL'],
    'temperature': config.getfloat("LLM", 'TEMPERATURE')
}

embedding_model_config = {
    'api_key': os.getenv(config['EMBEDDING_MODEL']['KEY']),
    'embedding_model': config['EMBEDDING_MODEL']['MODEL']
}

documents_config = {
    'chunk_size': config.getint('DOCUMENT_OPS', 'CHUNK_SIZE'),
    'chunk_overlap': config.getint('DOCUMENT_OPS', 'CHUNK_OVERLAP')
}

log_config = {
    'log_name': config['LOGGING']['LOG_NAME'],
    'log_dir': config['LOGGING']['LOG_DIR'],
    'log_file': config['LOGGING']['LOG_FILE'],
    'log_dest': f"{config['LOGGING']['LOG_DIR']}/{config['LOGGING']['LOG_FILE']}"
}

chromadb_config = {
    'chromadb_api_key': os.getenv(config['CHROMA_DB']['KEY']),
    'collection_name': config['CHROMA_DB']['COLLECTION_NAME'],
    'persist_directory': config['CHROMA_DB']['PERSIST_DIRECTORY'],
    'k': config['CHROMA_DB']['K']
}
