from fastapi import FastAPI, UploadFile, File
from dotenv import load_dotenv
from fastapi.responses import StreamingResponse

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



