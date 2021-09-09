import uvicorn

from typing import Optional

from pathlib import Path
from starlette.staticfiles import StaticFiles
from fastapi import FastAPI, HTTPException
import extract_settings
import yaml

app = FastAPI(docs_url="/openapi")

CONFIG_FILE = Path("/config/config.yaml")

FullSettings = extract_settings.get()


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}


@app.get("/api/v1/settings", response_model=FullSettings)
def get_settings():
    if not CONFIG_FILE.is_file():
        raise HTTPException(404, detail=f"Config file '{CONFIG_FILE}' is not a file")

    config_contents = yaml.load(CONFIG_FILE.read_text("utf-8"), Loader=yaml.SafeLoader)
    return FullSettings(**config_contents)


@app.put("/api/v1/settings")
def update_settings(settings: FullSettings):
    settings_to_write = settings.dict()
    yaml.dump(settings_to_write, CONFIG_FILE.open("w"))


app.mount(
    "/docs/",
    StaticFiles(directory=f"{Path(__file__).parent.resolve().parent}/docs/site", html=True),
    name="frontend",
)


app.mount(
    "/", StaticFiles(directory="frontend/build", html=True), name="frontend",
)


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=11102, log_level="info", reload=True)
