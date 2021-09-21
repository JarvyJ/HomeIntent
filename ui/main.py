from exceptions import HomeIntentHTTPException, http_exception_handler
from pathlib import Path

from broadcaster import Broadcast
from fastapi import FastAPI, Request, WebSocket
from pydantic import BaseModel, ValidationError
from starlette.concurrency import run_until_first_complete
from starlette.staticfiles import StaticFiles
import uvicorn

from routers import rhasspy, settings

broadcast = Broadcast("memory://")

app = FastAPI(
    docs_url="/openapi",
    title="Home Intent UI",
    description="A simple web interface to help manage Home Intent. NOTE: This API should be considered unstable",
    version="2021.10.0b1",
    on_startup=[broadcast.connect],
    on_shutdown=[broadcast.disconnect],
)


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
    await broadcast.publish(channel="logs", message=body.data)


@app.websocket("/ws/logs")
async def logs_ws(websocket: WebSocket):
    await websocket.accept()
    await run_until_first_complete((logs_ws_sender, {"websocket": websocket}),)


async def logs_ws_sender(websocket):
    async with broadcast.subscribe(channel="logs") as subscriber:
        async for event in subscriber:
            await websocket.send_text(event.message)


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
