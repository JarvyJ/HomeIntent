import json
from pathlib import Path
import sys
from typing import Optional

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import ValidationError
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


def pseudo_serialize_settings(settings_object):
    # use the json to serialize things a bit more sanely
    normalize = json.loads(settings_object.json(exclude_defaults=True))

    # remove unused keys to better match the yaml config file
    keys_to_remove = []
    for key in normalize:
        if not normalize[key] and key not in FullSettings.components_without_settings:
            keys_to_remove.append(key)

        if normalize[key] == "No-Value-Provided":
            keys_to_remove.append(key)

    for key in keys_to_remove:
        del normalize[key]

    return normalize


# displays any errors the user may have put into the config.yaml file manually
@app.exception_handler(ValidationError)
async def unicorn_exception_handler(request: Request, exc: ValidationError):
    return JSONResponse(
        status_code=400,
        content={"detail": exc.errors(), "title": "Something is wrong in /config/config.yaml"},
    )


@app.get("/api/v1/settings", response_model=FullSettings, response_model_exclude_unset=True)
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
    if config_contents:
        return FullSettings(**config_contents)
    else:
        return FullSettings()


@app.put("/api/v1/settings")
def update_settings(settings: FullSettings, response_model_exclude_unset=True):
    """
    You should probably read the GET /api/v1/settings caveat above.

    tl;dr: omit any key/values for things that are not enabled.
    """
    yaml = YAML()
    if CONFIG_FILE.is_file():
        config_contents = yaml.load(CONFIG_FILE.read_text("utf-8"))

        # this is really hokey and leaves a lot of room for improvements
        # the general idea is to not change what the user has manually done in config
        # the json loads/.json() is mostly to get pydantic to serialize everything
        # to happy types (ints/strings/etc) as yaml will try to serialize the classes
        # the merge should hopefully keep any comments/structure the user might have in place
        # this might cause issues in the future, but we'll try it for now!
        if config_contents:
            merge_dict(pseudo_serialize_settings(settings), config_contents)

        else:
            config_contents = pseudo_serialize_settings(settings)

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

    yaml.dump(config_contents, sys.stdout)
    return config_contents
    # yaml.dump(settings_to_write, CONFIG_FILE.open("w"))


app.mount(
    "/", StaticFiles(directory="frontend/build", html=True), name="frontend",
)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=11102, log_level="info", reload=True)
