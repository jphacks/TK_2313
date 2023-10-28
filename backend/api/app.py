from fastapi import FastAPI, UploadFile, File, WebSocket
from dotenv import load_dotenv
from fastapi.responses import StreamingResponse
import base64
import json
import handler

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


@app.websocket("/event/wav")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    rawData = await websocket.receive_bytes()
    # decode base64
    voice_input = base64.b64decode(rawData)
    voice_output = handler.handle_voice_driven(voice_input)

    base64str = str(base64.b64encode(voice_output[0]))
    response = {
        'audio': base64str,
        'text': voice_output[1]
    }

    await websocket.send_text(json.dumps(response))
    await websocket.close()


@app.websocket("/event/text")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Message text was: {data}")
        if data == "close":
            await websocket.close()
            break
