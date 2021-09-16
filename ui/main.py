from pathlib import Path
import sys

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from ruamel.yaml import YAML
from starlette.staticfiles import StaticFiles
import uvicorn

from extract_settings import ExtractSettings, merge, pseudo_serialize_settings

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


@app.put("/api/v1/settings", response_model=FullSettings, response_model_exclude_unset=True)
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
            reserialized_settings, components_to_remove = pseudo_serialize_settings(
                settings, FullSettings
            )
            merge(reserialized_settings, config_contents)

            # the merge doesn't delete any components that have been disabled,
            # so we need to disable them manually
            for component in components_to_remove:
                if component in config_contents:
                    del config_contents[component]

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
            components_to_remove = current_nosetting_components.difference(
                updated_nosetting_components
            )
            for component in components_to_remove:
                del config_contents[component]

        else:
            config_contents = pseudo_serialize_settings(settings, FullSettings)

    yaml.dump(config_contents, sys.stdout)
    return config_contents
    # yaml.dump(settings_to_write, CONFIG_FILE.open("w"))


app.mount(
    "/", StaticFiles(directory="frontend/build", html=True), name="frontend",
)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=11102, log_level="info", reload=True)
