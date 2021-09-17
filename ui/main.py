from pathlib import Path
import sys

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from ruamel.yaml import YAML
from starlette.staticfiles import StaticFiles
import uvicorn

from extract_settings import ExtractSettings, merge, pseudo_serialize_settings
from rhasspy_api import RhasspyAPI
import subprocess
from enum import Enum
from typing import Dict

app = FastAPI(
    docs_url="/openapi",
    title="Home Intent UI",
    description="A simple web interface to help manage Home Intent",
    version="2021.10.0b1",
)

app.mount(
    "/docs/",
    StaticFiles(directory=f"{Path(__file__).parent.resolve().parent}/docs/site", html=True),
    name="frontend",
)

CONFIG_FILE = Path("/config/config.yaml")
FullSettings = ExtractSettings.get()
SETTINGS = FullSettings(**YAML().load(CONFIG_FILE.read_text()))
RhasspyApi = RhasspyAPI(SETTINGS.rhasspy.url)


# displays any errors the user may have put into the config.yaml file manually
@app.exception_handler(ValidationError)
async def yaml_config_validation_handler(request: Request, exc: ValidationError):
    return JSONResponse(
        status_code=400,
        content={"detail": exc.errors(), "title": "Something is wrong in /config/config.yaml"},
    )


@app.get("/api/v1/settings", response_model=FullSettings, response_model_exclude_unset=True)
def get_settings():
    """
    The JSON version of `/config/config.yaml`

    For components _with_ settings, if it is enabled,
    then the value is the component's config object.
    If it is disabled, the key will not exist.

    For components _without_ settings, if the key is present it is enabled.
    The value should be `null`.

    Components with settings are defined in the OpenAPI spec.
    A list of components without settings are found in
    a helper object (`x-components-without-settings`) in `additionalProperties`

    """
    if not CONFIG_FILE.is_file():
        raise HTTPException(404, detail=f"Config file '{CONFIG_FILE}' is not a file")

    yaml = YAML()
    config_contents = yaml.load(CONFIG_FILE.read_text("utf-8"))
    if config_contents:
        return FullSettings(**config_contents)
    else:
        return FullSettings()


@app.post("/api/v1/settings", response_model=FullSettings, response_model_exclude_unset=True)
def update_settings(settings: FullSettings):
    """
    This endpoint will convert the JSON back to `/config/config.yaml` discarding any default values
    in an attempt to keep the config file more easily human editable.
    """
    yaml = YAML()
    if CONFIG_FILE.is_file():
        config_contents = yaml.load(CONFIG_FILE.read_text("utf-8"))

        # this is really hokey and leaves a lot of room for improvements
        # the general idea is to not change what the user has manually done in config
        # the merge should hopefully keep any comments/structure the user might have in place
        # this might cause issues in the future, but we'll try it for now!
        if config_contents:
            reserialized_settings, default_components_to_remove = pseudo_serialize_settings(
                settings, FullSettings
            )
            merge(reserialized_settings, config_contents)
            remove_unused_defaults_from_config(config_contents, default_components_to_remove)
            remove_disabled_nosettings_components_from_merged_config(config_contents, settings)

        else:
            config_contents = pseudo_serialize_settings(settings, FullSettings)

    yaml.dump(config_contents, sys.stdout)
    return config_contents
    # yaml.dump(settings_to_write, CONFIG_FILE.open("w"))


def remove_unused_defaults_from_config(config_contents, default_components_to_remove):
    for component in default_components_to_remove:
        if component in config_contents:
            del config_contents[component]


def remove_disabled_nosettings_components_from_merged_config(config_contents, settings):
    # code to figure out what components w/out settings are enabled
    current_nosetting_components = frozenset(
        key
        for key, value in config_contents.items()
        if value is None and key in FullSettings.components_without_settings
    )
    updated_nosetting_components = frozenset(
        key
        for key, value in settings.dict().items()
        if value is None and key in FullSettings.components_without_settings
    )

    # get away with a difference here because the update has already happened
    components_to_remove = current_nosetting_components.difference(updated_nosetting_components)
    for component in components_to_remove:
        del config_contents[component]


@app.get("/api/v1/rhasspy/audio/microphones")
def get_rhasspy_microphones(show_all: bool = False):
    rhasspy_microphones = RhasspyApi.get("/api/microphones")
    if show_all:
        return rhasspy_microphones
    else:
        small_list = {}
        for mic_id, name in rhasspy_microphones.items():
            if "(hw:" in name:
                small_list[mic_id] = name
        print(small_list)
        return small_list


@app.get("/api/v1/rhasspy/audio/speakers")
def get_rhasspy_speakers(show_all: bool = True):
    rhasspy_speakers = RhasspyApi.get("/api/speakers")
    if show_all:
        return rhasspy_speakers
    else:
        small_list = {}
        for speaker_id, name in rhasspy_speakers.items():
            if speaker_id.startswith("default:"):
                small_list[speaker_id] = name

        return small_list


@app.get("/api/v1/rhasspy/audio/test-speakers")
def test_speakers(device: str = None):
    output = play_file("./alarm2.wav", device)
    if output.returncode != 0:
        raise HTTPException(
            400,
            detail={
                "stdout": output.stdout.decode("utf-8"),
                "stderr": output.stderr.decode("utf-8"),
            },
        )


def play_file(file, device):
    if device:
        output = subprocess.run(
            ["aplay", "-D", device, "-t", "wav", file], check=False, capture_output=True
        )

    else:
        output = subprocess.run(["aplay", "-t", "wav", file], check=False, capture_output=True)

    return output


class SoundEffect(str, Enum):
    BEEP_HIGH = "beep_high"
    BEEP_LOW = "beep_low"
    ERROR = "error"


@app.get("/api/v1/rhasspy/audio/play-effects")
def play_effects(sound_effect: SoundEffect, device: str = None):
    filename = f"{sound_effect.value.replace('_', '-')}.wav"
    custom_file_path = Path("/config") / filename
    file_path = Path(__file__).parent.resolve().parent / "home_intent/default_configs" / filename

    if custom_file_path.is_file():
        play_file(custom_file_path, device)
    else:
        play_file(file_path, device)
    return file_path


class CustomOrDefault(str, Enum):
    CUSTOM = "custom"
    DEFAULT = "default"


@app.get("/api/v1/rhasspy/audio/effects", response_model=Dict[SoundEffect, CustomOrDefault])
def get_effects():
    output = {}
    for sound_effect in SoundEffect:
        filename = f"{sound_effect.value.replace('_', '-')}.wav"
        custom_file_path = Path("/config") / filename

        if custom_file_path.is_file():
            output[sound_effect] = CustomOrDefault.CUSTOM
        else:
            output[sound_effect] = CustomOrDefault.DEFAULT

    return output


app.mount(
    "/", StaticFiles(directory="frontend/build", html=True), name="frontend",
)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=11102, log_level="info", reload=True)
