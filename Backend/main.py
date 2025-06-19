from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from redis_pubsub import RedisPubSubManager
import json
import asyncio

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

manager = RedisPubSubManager()
connected_clients = []
pubsub_task = None   

@app.on_event("startup")
async def startup_event():
    await manager.subscribe()
    global pubsub_task
    pubsub_task = asyncio.create_task(redis_listener())   

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connected_clients.append(websocket)

    username = None

    try:
        while True:
            data = await websocket.receive_text()
            data_dict = json.loads(data)

            if data_dict["message"] == "__joined__":
                username = data_dict["username"]

            await manager.publish(data)

    except WebSocketDisconnect:
        connected_clients.remove(websocket)

        if username:
            leave_msg = json.dumps({
                "username": username,
                "message": "__left__"
            })
            await manager.publish(leave_msg)

async def redis_listener():
    async for message in manager.listen():
        for client in connected_clients:
            try:
                await client.send_text(message)
            except:
                pass
