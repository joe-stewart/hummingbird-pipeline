#!/usr/bin/env python3
"""
view_camera.py — Live view of reCamera stream
Run from NUC: python3 nuc/view_camera.py
Press 'q' to quit
"""
import asyncio
import base64
import json
import cv2
import numpy as np
import websockets

RECAMERA_WS = "ws://192.168.2.14:8090"

async def view():
    print(f"Connecting to {RECAMERA_WS} — press 'q' to quit")
    async with websockets.connect(RECAMERA_WS, ping_interval=None) as ws:
        while True:
            data = await ws.recv()
            msg = json.loads(data)
            image_b64 = msg.get("data", {}).get("image")
            if image_b64:
                jpg = base64.b64decode(image_b64)
                arr = np.frombuffer(jpg, dtype=np.uint8)
                frame = cv2.imdecode(arr, cv2.IMREAD_COLOR)
                if frame is not None:
                    cv2.imshow("reCamera", frame)
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break
    cv2.destroyAllWindows()

asyncio.run(view())
