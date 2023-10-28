from fastapi import FastAPI, UploadFile, File
from dotenv import load_dotenv

load_dotenv(verbose=True)


app = FastAPI()


@app.get("/ping")
async def pong():
    return {"ping": "pong!"}


@app.post("/upload/wav")
async def upload_wav(file: UploadFile = File(...)):
    # save file to ./tmp directory
    with open(f"./tmp/{file.filename}", "wb") as buffer:
        buffer.write(await file.read())
    return {"filename": file.filename}
