import time
import requests
import json
import asyncio
import websockets
import base64
import socket
from datetime import datetime
import os

# Stream ports
# 8090 - JSON + base64 JPEG 640x640 with inference overlay (current)
# 8080 - Raw H.264 1920x1080 for high quality training data (future)
NTFY_URL = "http://${RPI2_IP}:${NTFY_PORT}/bird/json"
RECAMERA_WS = "ws://${RECAMERA_IP}:${RECAMERA_WS_PORT}"
# RECAMERA_WS = "ws://${RECAMERA_IP}:8080"
ARDUINO_IP = "${ARDUINO_IP}"
SAVE_DIR = "/opt/hummingbird/frames"
ARDUINO_PORT = 8888
MAGIC = b"HUMM"

os.makedirs(SAVE_DIR, exist_ok=True)

def ping_arduino():
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(MAGIC, (ARDUINO_IP, ARDUINO_PORT))
        sock.close()
        print(f"Pinged Arduino at {ARDUINO_IP}:{ARDUINO_PORT}")
    except Exception as e:
        print(f"Arduino ping failed: {e}")

async def grab_frame():
    async with websockets.connect(RECAMERA_WS) as ws:
        data = await ws.recv()
        msg = json.loads(data)
        image_b64 = msg.get("data", {}).get("image")
        if image_b64:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{SAVE_DIR}/hummer_{timestamp}.jpg"
            with open(filename, "wb") as f:
                f.write(base64.b64decode(image_b64))
            print(f"Saved frame: {filename}")
            ping_arduino()

def listen():
    print("Listening for notifications...")
    while True:
        try:
            with requests.get(NTFY_URL, stream=True, timeout=60) as r:
                for line in r.iter_lines():
                    if line:
                        msg = json.loads(line)
                        if msg.get("event") == "message":
                            print(f"Got notification: {msg.get('message')}")
                            asyncio.run(grab_frame())
        except Exception as e:
            print(f"ntfy connection lost: {e}, retrying in 10s")
            time.sleep(10)
