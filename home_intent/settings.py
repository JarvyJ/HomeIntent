import os
from pathlib import Path
from typing import Any, Dict, Optional

from pydantic import AnyHttpUrl, BaseModel, BaseSettings, Field
import yaml

# diabled for the Settings object as pydantic passes init/env settings in
# pylint: disable=unused-argument


# the ISO639_1 codes supported in Rhasspy using Kaldi
# Source: https://rhasspy.readthedocs.io/en/latest/#supported-languages
ISO639_1 = frozenset(["en", "de", "es", "fr", "it", "nl", "ru", "vi", "sv", "cs"])


def yaml_config_settings_source(settings: BaseSettings) -> Dict[str, Any]:
    """
    A simple settings source that loads variables from a JSON file
    at the project's root.

    Here we happen to choose to use the `env_file_encoding` from Config
    when reading `config.json`
    """
    encoding = settings.__config__.env_file_encoding
    config_file = Path("/config/config.yaml")

    if config_file.is_file():
        return yaml.load(config_file.read_text(encoding), Loader=yaml.SafeLoader)
    else:
        return {}


class RhasspySettings(BaseModel):
    url: AnyHttpUrl = (
        "http://rhasspy:12101"
        if os.environ.get("DOCKER_DEV") == "True"
        else "http://localhost:12101"
    )
    mqtt_host: str = "rhasspy" if os.environ.get("DOCKER_DEV") == "True" else "localhost"
    mqtt_port: int = 12183
    mqtt_username: Optional[str] = None
    mqtt_password: Optional[str] = None
    microphone_device: Optional[str] = None
    sounds_device: Optional[str] = None
    externally_managed: bool = False


def get_env_language() -> str:
    set_language = os.environ.get("LANGUAGE")
    if set_language is None:
        return "en"

    # this is a bit of overkill and maybe not the best use of time
    iso639_1 = [x for x in set_language.split(":") if x in ISO639_1]
    if any(iso639_1):
        return iso639_1[0]

    return "en"


class HomeIntentSettings(BaseModel):
    beeps: bool = True
    enable_beta: bool = False
    enable_all: bool = False

    # there might be nested env var support one day: https://github.com/samuelcolvin/pydantic/pull/3159
    language: Optional[str] = Field(default_factory=get_env_language)


class Settings(BaseSettings):
    rhasspy: RhasspySettings = RhasspySettings()
    home_intent: HomeIntentSettings = HomeIntentSettings()

    class Config:  # pylint: disable=too-few-public-methods
        env_file_encoding = "utf-8"
        extra = "allow"

        @classmethod
        def customise_sources(
            cls,
            init_settings,
            env_settings,
            file_secret_settings,
        ):
            return (
                yaml_config_settings_source,
                file_secret_settings,
            )
