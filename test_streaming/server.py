import asyncio
import websockets
import cv2, base64
import numpy as np

async def accept(websocket, path):
    while True :
        data = await websocket.recv()
        img = cv2.imdecode(np.fromstring(base64.b64decode(data.split(',')[1]), np.uint8), cv2.IMREAD_COLOR)
        cv2.imshow('image', img)
        cv2.waitKey(1)
        #print("recv : " + data)
        #await websocket.send("echo : " + data)

server = websockets.serve(accept, "0.0.0.0", 9999)

asyncio.get_event_loop().run_until_complete(server)
asyncio.get_event_loop().run_forever()
