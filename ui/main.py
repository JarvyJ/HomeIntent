import json
from pathlib import Path
import sys
from typing import Optional

from fastapi import FastAPI, HTTPException
from ruamel.yaml import YAML
from starlette.staticfiles import StaticFiles
import uvicorn

import extract_settings

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

FullSettings = extract_settings.get()


def merge_dict(source, destination):
    for key, value in source.items():
        if isinstance(value, dict):
            # get node or create one
            node = destination.setdefault(key, {})
            merge_dict(value, node)
        else:
            destination[key] = value

    return destination


@app.get("/api/v1/settings", response_model=FullSettings)
def get_settings():
    """
    This endpoint ended up being accidentally obtuse...
    It does make sense for PUTting the new object back however.

    For components _with_ settings objets, the key (component name) is always present when
    getting settings and if it is disabled, the value is `null`.
    If it is enabled, then the value is the value of the component's config object.

    For components _without_ settings objects, if the key is present, then it is enabled.
    The value should be `null`.

    Yes, this means that `null` has two different meanings.
    This is mostly an artifact from storing the config as yaml and how it is represented in json.

    There is a helper object (`x-components-without-settings`) in `additionalProperties` that can
    be used to determine what components do not have settings objects.

    _However_, when updating the config object,
    you can just omit any keys (and values) that are not enabled.

    """
    if not CONFIG_FILE.is_file():
        raise HTTPException(404, detail=f"Config file '{CONFIG_FILE}' is not a file")

    yaml = YAML()
    config_contents = yaml.load(CONFIG_FILE.read_text("utf-8"))
    return FullSettings(**config_contents)


@app.put("/api/v1/settings")
def update_settings(settings: FullSettings):
    """
    You should probably read the GET /api/v1/settings caveat above.

    tl;dr: omit any key/values for things that are not enabled.
    """
    settings_to_write = settings.dict()
    for key, value in settings_to_write.items():
        if value is None:
            if key not in FullSettings.components_without_settings:
                raise HTTPException(
                    400, detail=f"The setting '{key}' is not a component that can be loaded."
                )

    yaml = YAML()
    if CONFIG_FILE.is_file():
        config_contents = yaml.load(CONFIG_FILE.read_text("utf-8"))

        # this is really hokey and leaves a lot of room for improvements
        # the general idea is to not change what the user has manually done in config
        # the json loads/.json() is mostly to get pydantic to serialize everything
        # to happy types (ints/strings/etc) as yaml will try to serialize the classes
        # the merge should hopefully keep any comments/structure the user might have in place
        # this might cause issues in the future, but we'll try it for now!
        reserialized_settings = json.loads(settings.json(exclude_defaults=True))
        merge_dict(reserialized_settings, config_contents)

        # code to figure out what components w/out settings are enabled
        current_nosetting_components = frozenset(
            key for key, value in config_contents.items() if value is None
        )
        updated_nosetting_components = frozenset(
            key for key, value in reserialized_settings.items() if value is None
        )

        # get away with a difference here because the update has already happened
        components_to_remove = current_nosetting_components.difference(updated_nosetting_components)
        for component in components_to_remove:
            del config_contents[component]

    yaml.dump(config_contents, sys.stdout)
    # yaml.dump(settings_to_write, CONFIG_FILE.open("w"))


app.mount(
    "/", StaticFiles(directory="frontend/build", html=True), name="frontend",
)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=11102, log_level="info", reload=True)
