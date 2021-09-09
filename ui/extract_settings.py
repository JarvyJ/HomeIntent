from functools import partial
import importlib
from pathlib import Path
import sys
from unittest.mock import MagicMock, patch

from pydantic import Field, create_model, BaseModel

PARENT_PATH = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PARENT_PATH))


class HealthyBreakpoint(Exception):
    pass


ALL_SETTINGS_OBJECTS = {}


def get() -> BaseModel:
    _get_default_settings()
    _crawl_and_get_component_settings()
    _crawl_and_get_custom_component_settings()
    return _generate_full_settings()


def _get_default_settings():
    from home_intent.settings import RhasspySettings, HomeIntentSettings

    ALL_SETTINGS_OBJECTS["home_intent"] = _create_dynamic_settings_object(HomeIntentSettings)
    ALL_SETTINGS_OBJECTS["rhasspy"] = _create_dynamic_settings_object(RhasspySettings)


def _crawl_and_get_component_settings():
    component_folder = PARENT_PATH / "home_intent/components"
    sys.path.append(str(component_folder))
    for init_file in sorted(component_folder.glob("*/__init__.py")):
        _get_settings_for_component(init_file.parts[-2])

    assert sys.path.pop() == str(component_folder)


def _crawl_and_get_custom_component_settings():
    sys.path.append("/config/custom_components")
    component_folder = Path("/config/custom_components")
    for init_file in sorted(component_folder.glob("*/__init__.py")):
        _get_settings_for_component(init_file.parts[-2])

    for init_file in sorted(component_folder.glob("*.py")):
        _get_settings_for_component(init_file.parts[-1][:-3])

    assert sys.path.pop() == "/config/custom_components"


def _get_settings_for_component(component_name, component_path=""):
    home_intent = MagicMock(name="home_intent")
    home_intent.get_config.side_effect = partial(_get_settings_object, component_name)
    component_prefix = f"{component_path}." if component_path else ""

    with patch.dict("sys.modules", home_intent=home_intent):
        integration = importlib.import_module(f"{component_prefix}{component_name}")
        try:
            integration.setup(home_intent)
        except HealthyBreakpoint:
            print("Got a settings object!")
        except Exception:
            pass


def _get_settings_object(name, settings_object):
    ALL_SETTINGS_OBJECTS[name] = _create_dynamic_settings_object(settings_object)
    raise HealthyBreakpoint("Found a settings object, no longer need to continue")


def _create_dynamic_settings_object(settings_object):
    # I pulled how to do this from
    # https://github.com/samuelcolvin/pydantic/issues/3184#issuecomment-914876226
    # it's a little odd, but seems to do the trick!

    return (settings_object, Field(default_factory=settings_object))


def _generate_full_settings():
    FullSettings = create_model("FullSettings", **ALL_SETTINGS_OBJECTS)

    return FullSettings


if __name__ == "__main__":
    generated_settings = get()
    print(generated_settings.schema_json(indent=2))
