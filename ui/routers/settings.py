import json
import sys
from pathlib import Path

from fastapi import APIRouter
from ruamel.yaml import YAML

from config import FullSettings, get_settings_async, CONFIG_FILE
from extract_settings import merge, pseudo_serialize_settings

router = APIRouter()


@router.get("/settings", response_model=FullSettings, response_model_exclude_unset=True)
async def get_settings():
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
    return await get_settings_async()


@router.post("/settings", response_model=FullSettings, response_model_exclude_unset=True)
def update_settings(settings: FullSettings):
    """
    This endpoint will convert the JSON back to `/config/config.yaml` discarding any default values
    in an attempt to keep the config file more easily human editable.
    """
    # TODO: eventually see if yaml.dump can support async file streams, until then, keep it sync

    yaml = YAML()
    config_file = Path(CONFIG_FILE)
    config_contents = pseudo_serialize_settings(settings, FullSettings)
    yaml.dump(config_contents, config_file.open("w"))
    return config_contents
