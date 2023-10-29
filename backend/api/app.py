from fastapi import FastAPI, UploadFile, File, WebSocket, WebSocketDisconnect
from dotenv import load_dotenv
from fastapi.responses import StreamingResponse
import base64
import json
import handler
import logging

load_dotenv(verbose=True)

app = FastAPI()


@app.get("/ping")
async def pong():
    return {"ping": "pong!"}


@app.post("/upload/wav")
async def upload_wav(file: UploadFile = File(...)):
    # save file to ./tmp directory
    with open(f"/tmp/{file.filename}", "wb") as buffer:
        buffer.write(await file.read())

    stream = handler.handle_voice_driven(f"/tmp/{file.filename}")
    # save to /tmp


class ConnectionManager:
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


manager = ConnectionManager()


@app.websocket("/event")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            rawData = await websocket.receive_text()
            input = json.loads(rawData)

            # check kind types (send_wav, receive_wav, send_text, receive_text)

            if input["kind"] == "near_anchor":
                response = handler.handle_anchor_driven(input["anchor_id"])
                if response is None:
                    continue
                

                await websocket.send_text(json.dumps(response))

            if input["kind"] == "send_wav":
                voice_input = base64.b64decode(input["base64"])
                voice_output = handler.handle_voice_driven(voice_input)

                base64str = str(base64.b64encode(voice_output[0]))
                # remove b' and ' from base64str
                base64str = base64str[2:-1]

                response = {
                    'kind': "receive_wav",
                    'base64': base64str,
                    'text': voice_output[1]
                }

                await websocket.send_text(json.dumps(response))
    except WebSocketDisconnect:
        logging.info("Client left")
