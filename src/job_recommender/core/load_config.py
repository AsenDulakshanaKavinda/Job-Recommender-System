# E:\Project\Job-Recommender-System\src\job_recommender\core\load_config.py

from pathlib import Path
import os
import yaml
import logging
from src.job_recommender.core.settings import Settings


class LoadConfig:
    def __init__(self, env: str | None = None, config_path: str | None = None):
        """
        env: 'dev'or 'prod' (default: 'dev')
        config_path: override path to YAML config
        """

        self.project_root = self._get_project_root()

        # determine env
        env = env or os.getenv("ENV") or "dev"

        # determine env
        if config_path:
            path = Path(config_path)
        else:
            env_path = os.getenv("CONFIG_PATH")
            path = Path(env_path) if env_path else Path("config") / f"config.{env}.yaml"
        
        # if the path is relavent, make it absolute relative to project root
        if not path.is_absolute():
            path = self.project_root / path

        # validate file existence
        self._ensure_config_file_exists(path)

        # load yaml file
        self.raw_config = self._load_yaml_file(path)

        # validate and parse with pydantic
        self.config = Settings(**self.raw_config)

        self.config_path = path

        self._setup_logging()
        print(f"Loaded successfully from {path} (env={env})")

    

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
        if not path.exists():
            raise FileNotFoundError(f"Config file not found: {str(path)}")

    def _load_yaml_file(self, path: Path) -> dict:
        with open(path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f) or {}
        
    def _setup_logging(self):
        log_cfg = self.config.logging
        level = getattr(logging, log_cfg.level)
        # logging.basicConfig(filename=log_cfg.filepath, level=level, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s") - if use a file


