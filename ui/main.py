from exceptions import HomeIntentHTTPException, http_exception_handler
from pathlib import Path
from typing import List

from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from pydantic import BaseModel, ValidationError
from starlette.staticfiles import StaticFiles
import uvicorn

from routers import rhasspy, settings

app = FastAPI(
    docs_url="/openapi",
    title="Home Intent UI",
    description="A simple web interface to help manage Home Intent. NOTE: This API should be considered unstable",
    version="2021.10.0b1",
)


# I normally don't have too much fun with classnames, but this one was too good to pass up.
class SocketMan:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)


# see look, the instantiated class is boring and descriptive again
websocket_manager = SocketMan()


@app.exception_handler(HomeIntentHTTPException)
async def home_intent_http_exception_handler(request, exc):
    return await http_exception_handler(request, exc)


# displays any errors the user may have put into the config.yaml file manually
@app.exception_handler(ValidationError)
async def yaml_config_validation_handler(request: Request, exc: ValidationError):
    error_message = "; ".join(str(exc).split("\n")[1:])
    home_intent_exception = HomeIntentHTTPException(
        400, title=f"Validation error in /config/config.yaml: {error_message}", detail=exc.errors()
    )
    return await http_exception_handler(request, home_intent_exception)


app.include_router(settings.router, prefix="/api/v1", tags=["Settings"])
app.include_router(rhasspy.router, prefix="/api/v1", tags=["Rhasspy Audio"])


class LogFormat(BaseModel):
    data: str


@app.post("/api/v1/logs")
async def handle_logs(body: LogFormat):
    await websocket_manager.broadcast(body.data)


@app.websocket("/ws/logs")
async def logs_ws(websocket: WebSocket):
    await websocket_manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()

    except WebSocketDisconnect:
        websocket_manager.disconnect(websocket)


app.mount(
    "/docs/",
    StaticFiles(directory=Path(__file__).parent.resolve().parent / "docs/site", html=True),
    name="frontend",
)

app.mount(
    "/",
    StaticFiles(directory=Path(__file__).parent.resolve() / "frontend/build", html=True),
    name="frontend",
)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=11102, log_level="info", reload=True)
