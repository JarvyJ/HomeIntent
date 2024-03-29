import json
from pathlib import Path
from typing import Any, Dict

from pydantic import BaseSettings

from home_intent.constants import VERSION


def json_config_settings_source(settings: BaseSettings) -> Dict[str, Any]:
    """
    A simple settings source that loads variables from a JSON file
    at the project's root.

    Here we happen to choose to use the `env_file_encoding` from Config
    when reading `config.json`
    """
    encoding = settings.__config__.env_file_encoding
    meta_file_path = Path("/config/home_intent_meta.json")
    if meta_file_path.is_file():
        return json.loads(meta_file_path.read_text(encoding))
    else:
        return {}


class HomeIntentMeta(BaseSettings):
    last_run_version: str = VERSION

    def save(self):
        config_dir = Path("/config")
        meta_file_path = config_dir / "home_intent_meta.json"

        if not config_dir.is_dir():
            config_dir.mkdir()

        meta_file_path.write_text(self.json(indent=2), encoding="utf-8")

    class Config:
        env_file_encoding = "utf-8"

        @classmethod
        def customise_sources(
            cls, init_settings, env_settings, file_secret_settings,
        ):
            return (
                init_settings,
                json_config_settings_source,
            )
