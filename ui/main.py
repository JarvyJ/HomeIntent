from typing import Optional

from pathlib import Path
from starlette.staticfiles import StaticFiles
from fastapi import FastAPI

app = FastAPI(docs_url="/openapi")

print(f"{Path(__file__).parent.resolve().parent}/docs/site")


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}


app.mount(
    "/", StaticFiles(directory="frontend/build", html=True), name="frontend",
)

app.mount(
    "/docs/",
    StaticFiles(directory=f"{Path(__file__).parent.resolve().parent}/docs/site", html=True),
    name="frontend",
)
