import websockets
import asyncio
import base64
import data_url


async def hello():
    uri = "ws://localhost:3000/event/wav"
    fname = "output2.wav"
    with open(fname, "rb") as f:
        data = f.read()
    s = data_url.construct_data_url(
        mime_type='audio/wav', base64_encode=True, data=data)
    print(s)
    async with websockets.connect(uri) as websocket:
        await websocket.send(s)
        await websocket.close()

asyncio.get_event_loop().run_until_complete(hello())
