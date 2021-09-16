from functools import partial
import importlib
import json
from pathlib import Path
import sys
from typing import ClassVar, FrozenSet, Optional
from unittest.mock import MagicMock, patch

from pydantic import BaseModel, Field, create_model, validator

PARENT_PATH = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PARENT_PATH))


class _HealthyBreakpoint(Exception):
    pass


# Default class for
class _Missing:
    def __init__(self):
        pass

    def __str__(self):
        return "No-Value-Provided"

    def __repr__(self):
        return "No-Value-Provided"


class SettingsConfig:  # pylint: disable=too-few-public-methods
    extra = "allow"
    json_encoders = {
        _Missing: str,
    }


# used to ensure that components with settings don't come in with None
def _validate_not_none(cls, value):  # pylint: disable=unused-argument
    assert value is not None, "must not be None"
    return value


class ExtractSettings:
    ALL_SETTINGS_OBJECTS = {}
    VALIDATORS = {}
    COMPONENTS_WITHOUT_SETTINGS = set()
    CUSTOM_COMPONENTS = set()

    @classmethod
    def get(cls) -> BaseModel:
        cls._get_default_settings()
        cls._crawl_and_get_component_settings()
        cls._crawl_and_get_custom_component_settings()
        return cls._generate_full_settings()

    @classmethod
    def _get_default_settings(cls):
        from home_intent.settings import (  # pylint: disable=import-outside-toplevel
            RhasspySettings,
            HomeIntentSettings,
        )

        cls.ALL_SETTINGS_OBJECTS["home_intent"] = cls._create_dynamic_settings_object(
            HomeIntentSettings
        )
        cls.ALL_SETTINGS_OBJECTS["rhasspy"] = cls._create_dynamic_settings_object(RhasspySettings)

    @classmethod
    def _crawl_and_get_component_settings(cls):
        component_folder = PARENT_PATH / "home_intent/components"
        sys.path.append(str(component_folder))
        for init_file in sorted(component_folder.glob("*/__init__.py")):
            component_name = init_file.parts[-2]
            cls._get_settings_for_component(component_name)

        assert sys.path.pop() == str(component_folder)

    @classmethod
    def _crawl_and_get_custom_component_settings(cls):
        sys.path.append("/config/custom_components")
        component_folder = Path("/config/custom_components")
        for init_file in sorted(component_folder.glob("*/__init__.py")):
            component_name = init_file.parts[-2]
            cls._get_settings_for_component(component_name)
            cls.CUSTOM_COMPONENTS.add(component_name)

        for init_file in sorted(component_folder.glob("*.py")):
            component_name = init_file.parts[-1][:-3]
            cls._get_settings_for_component(component_name)
            cls.CUSTOM_COMPONENTS.add(component_name)

        assert sys.path.pop() == "/config/custom_components"

    @classmethod
    def _get_settings_for_component(cls, component_name, component_path=""):
        home_intent = MagicMock(name="home_intent")
        home_intent.get_config.side_effect = partial(cls._get_settings_object, component_name)
        component_prefix = f"{component_path}." if component_path else ""

        no_settings_component = True

        with patch.dict("sys.modules", home_intent=home_intent):
            integration = importlib.import_module(f"{component_prefix}{component_name}")
            try:
                integration.setup(home_intent)
            except _HealthyBreakpoint:
                no_settings_component = False

            # eventually it will break because the Mock can't handle it
            except Exception:  # pylint: disable=broad-except
                pass

        if no_settings_component:
            cls.COMPONENTS_WITHOUT_SETTINGS.add(component_name)

    @classmethod
    def _get_settings_object(cls, name, settings_object):
        cls.ALL_SETTINGS_OBJECTS[name] = cls._create_dynamic_settings_object(
            settings_object, optional=True
        )
        cls.VALIDATORS[f"{name}_validator"] = validator(name, allow_reuse=True, pre=True)(
            _validate_not_none
        )
        raise _HealthyBreakpoint("Found a settings object, no longer need to continue")

    @classmethod
    def _create_dynamic_settings_object(cls, settings_object, optional=False):
        # I pulled how to do this from
        # https://github.com/samuelcolvin/pydantic/issues/3184#issuecomment-914876226
        # it's a little odd, but seems to do the trick!

        if optional:
            return (Optional[settings_object], Field(default_factory=_Missing))
        else:
            return (settings_object, Field(default_factory=settings_object))

    @classmethod
    def _generate_full_settings(cls):
        SettingsConfig.schema_extra = {
            "additionalProperties": {
                "x-components-without-settings": cls.COMPONENTS_WITHOUT_SETTINGS,
                "x-custom-components": cls.CUSTOM_COMPONENTS,
            }
        }
        full_settings = create_model(
            "FullSettings",
            **cls.ALL_SETTINGS_OBJECTS,
            __config__=SettingsConfig,
            components_without_settings=(
                ClassVar[FrozenSet],
                frozenset(cls.COMPONENTS_WITHOUT_SETTINGS),
            ),
            __validators__=cls.VALIDATORS,
        )

        return full_settings


def merge(source, destination):
    for key, value in source.items():
        if isinstance(value, dict):
            # get node or create one
            node = destination.setdefault(key, {})
            merge(value, node)
        else:
            destination[key] = value

    return destination


def pseudo_serialize_settings(settings_object, settings_schema):
    # the json loads/.json() is mostly to get pydantic to serialize everything
    # to happy types (ints/strings/etc) as yaml will try to serialize the classes
    normalize = json.loads(settings_object.json(exclude_defaults=True))

    # remove unused keys to better match the yaml config file
    keys_to_remove = []
    for key in normalize:
        if key not in settings_schema.components_without_settings and not normalize[key]:
            keys_to_remove.append(key)

        if normalize[key] == "No-Value-Provided":
            keys_to_remove.append(key)

    print(keys_to_remove)

    for key in keys_to_remove:
        del normalize[key]

    return normalize, keys_to_remove


if __name__ == "__main__":
    generated_settings = ExtractSettings.get()
    print(generated_settings.schema_json(indent=2))

    from ruamel.yaml import YAML

    yaml = YAML()

    CONFIG_FILE = Path("/config/config.yaml")
    config_contents = yaml.load(CONFIG_FILE.read_text("utf-8"))
    if config_contents:
        going_back = generated_settings(**config_contents)
        print(going_back)
    else:
        going_back = generated_settings()

    # this is really hokey and leaves a lot of room for improvements
    # the general idea is to not change what the user has manually done in config
    # the json loads/.json() is mostly to get pydantic to serialize everything
    # to happy types (ints/strings/etc) as yaml will try to serialize the data types
    if config_contents:
        going_back.my_crazy_custom_component = True
        merge(pseudo_serialize_settings(going_back, generated_settings), config_contents)
    else:
        config_contents = pseudo_serialize_settings(going_back, generated_settings)

    yaml.dump(config_contents, sys.stdout)
