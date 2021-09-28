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

    if config_file.is_file():
        config_contents = yaml.load(config_file.read_text("utf-8"))

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
    # yaml.dump(settings_to_write, config_file.open("w"))


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
