from pathlib import Path
from typing import Any, Dict, Optional

from pydantic import AnyHttpUrl, BaseModel, BaseSettings
import yaml

# diabled for the Settings object as pydantic passes init/env settings in
# pylint: disable=unused-argument


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
    url: AnyHttpUrl = "http://localhost:12101"
    mqtt_host: str = "localhost"
    mqtt_port: int = 12183
    mqtt_username: Optional[str] = None
    mqtt_password: Optional[str] = None
    microphone_device: Optional[str] = None
    sounds_device: Optional[str] = None


class HomeIntentSettings(BaseModel):
    beeps: bool = True
    enable_beta: bool = False
    enable_all: bool = False


class Settings(BaseSettings):
    rhasspy: RhasspySettings = RhasspySettings()
    home_intent: HomeIntentSettings = HomeIntentSettings()

    class Config:  # pylint: disable=too-few-public-methods
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
