from collections import defaultdict
from typing import Dict, List
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


class LogFormat(BaseModel):
    data: str


# I could use some DI to get the websocket_manager into here, but for now I'm going to leave
# this here. If the websocket stuff starts getting out of hand, I'll start splitting it apart
@router.post("/api/v1/logs")
async def push_logs_to_websocket(body: LogFormat):
    await websocket_manager.broadcast("logs", body.data)


@router.websocket("/ws/logs")
async def logs_ws(websocket: WebSocket):
    await websocket_manager.connect("logs", websocket)
    try:
        while True:
            data = await websocket.receive_text()

    except WebSocketDisconnect:
        websocket_manager.disconnect("logs", websocket)


@router.post("/api/v1/jobs/restart")
async def update_restart_status(body: LogFormat):
    await websocket_manager.broadcast("jobs/restart", body.data)


@router.websocket("/ws/jobs/restart")
async def logs_ws(websocket: WebSocket):
    await websocket_manager.connect("jobs/restart", websocket)
    try:
        while True:
            data = await websocket.receive_text()

    except WebSocketDisconnect:
        websocket_manager.disconnect("jobs/restart", websocket)
