import json
from pathlib import Path
from typing import Any, Dict, Optional

from pydantic import AnyHttpUrl, BaseModel, BaseSettings
import yaml


def json_config_settings_source(settings: BaseSettings) -> Dict[str, Any]:
    """
    A simple settings source that loads variables from a JSON file
    at the project's root.

    Here we happen to choose to use the `env_file_encoding` from Config
    when reading `config.json`
    """
    encoding = settings.__config__.env_file_encoding
    return yaml.load(Path("/config/config.yaml").read_text(encoding), Loader=yaml.SafeLoader)


class RhasspySettings(BaseModel):
    url: AnyHttpUrl = "http://rhasspy:12101"
    mqtt_host: str = "rhasspy"
    mqtt_port: int = 12183
    mqtt_username: Optional[str] = None
    mqtt_password: Optional[str] = None


class Settings(BaseSettings):
    rhasspy: RhasspySettings = RhasspySettings()

    class Config:
        env_file_encoding = "utf-8"
        extra = "allow"

        @classmethod
        def customise_sources(
            cls, init_settings, env_settings, file_secret_settings,
        ):
            return (
                json_config_settings_source,
                file_secret_settings,
            )
