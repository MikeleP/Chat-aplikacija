from fastapi import FastAPI, WebSocket, WebSocketDisconnect

from fastapi.middleware.cors import CORSMiddleware

import json


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_methods=["*"],
    allow_headers=["*"],
)

connected_clients = []

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    client = {"socket": websocket, "username": None}
    connected_clients.append(client)

    try:
        while True:
            data = await websocket.receive_text()
            data_dict = json.loads(data)

            if data_dict["message"] == "__joined__":
                client["username"] = data_dict["username"]

            for c in connected_clients:
                await c["socket"].send_text(data)

    except WebSocketDisconnect:
        connected_clients.remove(client)

        if client["username"]:
            leave_msg = json.dumps({
                "username": client["username"],
                "message": "__left__"
            })
            for c in connected_clients:
                await c["socket"].send_text(leave_msg)


