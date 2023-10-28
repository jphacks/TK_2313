import websockets
import asyncio
import base64
import json
# import data_url


async def hello():
    # uri = "ws://localhost:8000/event/wav"
    uri = "wss://k1hmbp.tail5590e.ts.net/event/wav"
    fname = "output2.wav"
    with open(fname, "rb") as f:
        data = f.read()
    s = str(base64.b64encode(data))
    # remove b' and ' from string
    s = s[2:-1]
    request = {
        "kind": "send_wav",
        "base64": s
    }

    async with websockets.connect(uri) as websocket:
        await websocket.send(json.dumps(request))
        print(await websocket.recv())
        await websocket.close()

asyncio.get_event_loop().run_until_complete(hello())
