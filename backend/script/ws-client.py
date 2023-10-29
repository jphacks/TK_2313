import websockets
import asyncio
import base64
import json
from dotenv import load_dotenv
import pyaudio
import os
import wave

load_dotenv(verbose=True)


async def hello():
    uri = os.getenv("WS_URI")
    async with websockets.connect(uri) as websocket:

        # 音声をマイクから取得する
        # 1. 音声を5秒間録音する
        while True:
            audio = pyaudio.PyAudio()
            stream = audio.open(format=pyaudio.paInt16,
                                channels=1,
                                rate=16000,
                                input=True,
                                frames_per_buffer=1024)
            print("recording...")
            frames = []
            for i in range(0, int(16000 / 1024 * 5)):
                data = stream.read(1024)
                frames.append(data)
            print("finished recording")

            # 2. 録音した音声をファイルに保存する
            fname = os.getenv("FILE_NAME")
            wf = wave.open(fname, 'wb')
            wf.setnchannels(1)
            wf.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
            wf.setframerate(16000)
            wf.writeframes(b''.join(frames))
            wf.close()

            fname = os.getenv("FILE_NAME")
            with open(fname, "rb") as f:
                data = f.read()
            s = str(base64.b64encode(data))
            # remove b' and ' from string
            s = s[2:-1]
            request = {
                "kind": "send_wav",
                "base64": s
            }
            
            await websocket.send(json.dumps(request))
            response_raw = await websocket.recv()

            # Base64 decodeして再生する
            res = json.loads(response_raw)
            print(res["text"])
            decoded = base64.b64decode(res["base64"])
            fname = os.getenv("FILE_NAME")
            with open(fname, "wb") as f:
                f.write(decoded)
            wf = wave.open(fname, 'rb')
            p = pyaudio.PyAudio()
            stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                            channels=wf.getnchannels(),
                            rate=wf.getframerate(),
                            output=True)
            data = wf.readframes(1024)
            while data != b'':
                stream.write(data)
                data = wf.readframes(1024)
            stream.close()
            p.terminate()

asyncio.get_event_loop().run_until_complete(hello())
