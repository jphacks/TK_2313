import websockets
import asyncio
import base64
#import data_url


async def hello():
    uri = "ws://localhost:8000/event/wav"
    fname = "output2.wav"
    with open(fname, "rb") as f:
        data = f.read()
    s = base64.b64encode(data)
    async with websockets.connect(uri) as websocket:
        await websocket.send(s)
        print(await websocket.recv())
        # await websocket.close()

asyncio.get_event_loop().run_until_complete(hello())
