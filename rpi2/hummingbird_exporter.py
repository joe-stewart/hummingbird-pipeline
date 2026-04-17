#!/usr/bin/env python3
"""
hummingbird_exporter.py — Prometheus metrics for hummingbird detection pipeline
Subscribes to ntfy detection stream, exposes metrics on :9101
"""
import json
import time
import threading
import subprocess
import requests
from prometheus_client import start_http_server, Counter, Gauge

NTFY_URL     = "http://localhost:8080/bird/json"
METRICS_PORT = 9101
RECAMERA     = "recamera"
TEMP_INTERVAL = 900  # 15 minutes

detections_total = Counter(
    'hummingbird_detections_total',
    'Total number of hummingbird detection events'
)
last_detection_timestamp = Gauge(
    'hummingbird_last_detection_timestamp_seconds',
    'Unix timestamp of last detection event'
)
recamera_temperature = Gauge(
    'recamera_temperature_celsius',
    'reCamera SoC temperature in Celsius'
)

def collect_temp():
    while True:
        try:
            result = subprocess.run(
                ["ssh", "-o", "StrictHostKeyChecking=no", RECAMERA,
                 "cat /sys/class/thermal/thermal_zone0/temp"],
                capture_output=True, text=True, timeout=10
            )
            if result.returncode == 0:
                temp_c = int(result.stdout.strip()) / 1000.0
                recamera_temperature.set(temp_c)
                print(f"reCamera temp: {temp_c}°C")
            else:
                print(f"Temp read failed: {result.stderr}")
        except Exception as e:
            print(f"Temp collection error: {e}")
        time.sleep(TEMP_INTERVAL)

def listen():
    print(f"Starting hummingbird exporter on :{METRICS_PORT}")
    start_http_server(METRICS_PORT)
    t = threading.Thread(target=collect_temp, daemon=True)
    t.start()
    print(f"Listening for detections on {NTFY_URL}")
    while True:
        try:
            with requests.get(NTFY_URL, stream=True, timeout=60) as r:
                for line in r.iter_lines():
                    if line:
                        msg = json.loads(line)
                        if msg.get("event") == "message":
                            detections_total.inc()
                            last_detection_timestamp.set(time.time())
                            print(f"Detection recorded: {time.strftime('%Y-%m-%d %H:%M:%S')}")
        except Exception as e:
            print(f"Connection lost: {e}, retrying in 10s")
            time.sleep(10)

if __name__ == "__main__":
    listen()
