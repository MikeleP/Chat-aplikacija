from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from broadcaster import Broadcast
import asyncio
import json

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

broadcast = Broadcast("redis://localhost:6379")

@app.on_event("startup")
async def startup():
    await broadcast.connect()

@app.on_event("shutdown")
async def shutdown():
    await broadcast.disconnect()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    username = None  

    async def event_listener():
        async with broadcast.subscribe(channel="chat") as subscriber:
            async for event in subscriber:
                await websocket.send_text(event.message)

    listener_task = asyncio.create_task(event_listener())

    try:
        while True:
            data = await websocket.receive_text()
            data_dict = json.loads(data)

            if data_dict["message"] == "__joined__":
                username = data_dict["username"]

            await broadcast.publish(channel="chat", message=data)
    except WebSocketDisconnect:
        listener_task.cancel()

        if username:
            leave_msg = json.dumps({
                "username": username,
                "message": "__left__"
            })
            await broadcast.publish(channel="chat", message=leave_msg)
