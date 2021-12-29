from collections import defaultdict, deque
from exceptions import HomeIntentHTTPException
from pathlib import Path
import subprocess
from typing import Dict, List, Deque
from enum import Enum

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from pydantic import BaseModel

router = APIRouter()

# I normally don't have too much fun with classnames, but this one was too good to pass up.
class SocketMan:
    def __init__(self):
        self.active_connections: Dict[str, List[WebSocket]] = defaultdict(list)

    async def connect(self, channel: str, websocket: WebSocket):
        await websocket.accept()
        self.active_connections[channel].append(websocket)

    def disconnect(self, channel: str, websocket: WebSocket):
        self.active_connections[channel].remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, channel: str, message: str):
        for connection in self.active_connections[channel]:
            await connection.send_text(message)


# see look, the instantiated class is boring and descriptive again
websocket_manager = SocketMan()


class LogLevel(str, Enum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class LogFormat(BaseModel):
    data: str
    log_level: LogLevel
    time: float
    logger: str


exceptions: Deque[LogFormat] = deque(maxlen=32)
logs: Deque[LogFormat] = deque(maxlen=1024)

# I could use some DI to get the websocket_manager into here, but for now I'm going to leave
# this here. If the websocket stuff starts getting out of hand, I'll start splitting it apart
@router.post("/api/v1/logs")
async def push_logs_to_websocket(body: LogFormat):
    print(body)
    await websocket_manager.broadcast("logs", body.data)
    logs.append(body)
    if body.log_level in (LogLevel.WARNING, LogLevel.ERROR, LogLevel.CRITICAL):
        await websocket_manager.broadcast("exceptions", body.data)
        exception_message = body.data.split("\nTraceback", 1)[0]
        exceptions.append(
            LogFormat(
                data=exception_message, log_level=body.log_level, time=body.time, logger=body.logger
            )
        )


@router.get("/api/v1/logs", response_model=List[LogFormat])
def get_logs():
    return logs


@router.get("/api/v1/exceptions", response_model=List[LogFormat])
def get_exceptions():
    return exceptions


@router.websocket("/ws/logs")
async def logs_ws(websocket: WebSocket):
    await websocket_manager.connect("logs", websocket)
    try:
        while True:
            data = await websocket.receive_text()

    except WebSocketDisconnect:
        websocket_manager.disconnect("logs", websocket)


@router.websocket("/ws/exceptions")
async def exceptions_ws(websocket: WebSocket):
    await websocket_manager.connect("exceptions", websocket)
    try:
        while True:
            data = await websocket.receive_text()

    except WebSocketDisconnect:
        websocket_manager.disconnect("exceptions", websocket)


# TODO: get my dependency injection working, and get this out of here!
@router.get("/api/v1/restart", status_code=201)
async def restart_home_intent():
    # supervisorctl -c /usr/src/app/setup/supervisord.conf restart home_intent
    path = Path(__file__).parent.resolve().parent.parent / "setup/supervisord.conf"
    await websocket_manager.broadcast("jobs/restart", "Restarting the Home Intent process...")
    output = subprocess.run(
        ["supervisorctl", "-c", path, "restart", "home_intent"], check=False, capture_output=True
    )
    if output.returncode != 0:
        await websocket_manager.broadcast(
            "jobs/restart", f"Error restarting Home Intent: {output.stdout.decode('utf-8')}"
        )
        raise HomeIntentHTTPException(
            400,
            title="Error while restarting Home Intent",
            detail={
                "supervisord.conf": str(path),
                "stdout": output.stdout.decode("utf-8"),
                "stderr": output.stderr.decode("utf-8"),
            },
        )

    await websocket_manager.broadcast("jobs/restart", "Process has been started...")


@router.post("/api/v1/jobs/restart")
async def update_restart_status(body: LogFormat):
    await websocket_manager.broadcast("jobs/restart", body.data)


@router.websocket("/ws/jobs/restart")
async def restart_ws(websocket: WebSocket):
    await websocket_manager.connect("jobs/restart", websocket)
    try:
        while True:
            data = await websocket.receive_text()

    except WebSocketDisconnect:
        websocket_manager.disconnect("jobs/restart", websocket)
