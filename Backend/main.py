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

@app.on_event("startup")
async def startup_event():
    await manager.subscribe()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connected_clients.append(websocket)

    redis_listener_task = asyncio.create_task(redis_listener(websocket))

    try:
        while True:
            data = await websocket.receive_text()
            await manager.publish(data)

    except WebSocketDisconnect:
        connected_clients.remove(websocket)
        redis_listener_task.cancel()

async def redis_listener(websocket: WebSocket):
    async for message in manager.listen():
        for client in connected_clients:
            try:
                await client.send_text(message)
            except:
                pass
