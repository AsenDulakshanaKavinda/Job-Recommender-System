# E:\Project\Job-Recommender-System\src\job_recommender\core\load_config.py

from pathlib import Path
import os
import yaml
import logging
from datetime import datetime
import uuid

def generate_session_id() -> str:
    """"
    generate a unique session ID based on the current timestamp
    and random 8-character uuid format
    eg:-
        session_20250115_153045_a1b2c3d4
    """
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    unique_id = uuid.uuid4().hex[:8]
    return f"session_{timestamp}_{unique_id}"

class ProjectConfig:
    def __init__(self, env_provider: str | None = None, config_path: str | None = None):
        """
        env: 'dev'or 'prod' (default: 'dev')
        config_path: override path to YAML config
        """

        self._project_root = self._get_project_root()

        # determine env
        env_provider = env_provider or os.getenv("ENV") or "dev"

        # determine env
        if config_path:
            path = Path(config_path)
        else:
            env_path = os.getenv("CONFIG_PATH")
            path = Path(env_path) if env_path else Path("config") / f"config.{env_provider}.yaml"
        
        # if the path is relavent, make it absolute relative to project root
        if not path.is_absolute():
            path = self._project_root / path

        # validate file existence
        self._ensure_config_file_exists(path)

        # load yaml file
        self._raw_config = self._load_yaml_file(path)

        # todo --- use pydantic to validate this ---
        # validate and parse with pydantic
        # self.config = Settings(**self._raw_config)

        # project config
        self.config = self._raw_config 

        # config path
        self.config_path = path

        # self._setup_logging()
        print(f"Loaded successfully from {path} (env={env_provider})")


    def _get_project_root(self) -> Path:
        """ project root = 3 dirs above this file """
        return Path(__file__).resolve().parents[3]

    def _read_env_config_path(self):
        """ return CONFIG_PATH from env if exists """
        return os.getenv("CONFIG_PATH")
    
    def _default_config_path(self) -> Path:
        """ fallback to a default config file location """
        return Path("config" / "config.yaml")

    def _ensure_config_file_exists(self, path: Path):
        """ check whether config file exists or not """
        if not path.exists():
            raise FileNotFoundError(f"Config file not found: {str(path)}")

    def _load_yaml_file(self, path: Path) -> dict:
        """ read and return the data in yaml file as a dict """
        with open(path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f) or {}
        
    def _setup_logging(self):
        log_cfg = self.config.logging
        level = getattr(logging, log_cfg.level)
        # logging.basicConfig(filename=log_cfg.filepath, level=level, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s") - if use a file

project_config = ProjectConfig()
session_id = generate_session_id()
