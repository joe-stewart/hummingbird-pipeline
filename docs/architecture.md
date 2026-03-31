# Architecture

## Flow
```
reCamera (sensor + inference)
    ↓
Jetson (orchestration + capture)
    ↓              ↓
  NUC           Arduino R4
(viewing)        (alerting)
    ↑
  RPi2
(ntfy broker)
```

## Components

### reCamera
- OV5647 sensor, fixed focus ~1m to infinity
- sscma-node runs CV inference
- Publishes detections to Mosquitto
- Streams annotated JPEG over WebSocket :8090
- bird_watch.py — watches for detections, sends ntfy with 60s cooldown

### Jetson
- capture.py — listens to ntfy, grabs frame from reCamera WS, saves JPEG
- Runs as systemd service under hummingbird user
- Sends UDP heartbeat to Arduino every 5 min
- Frames saved to /opt/hummingbird/frames/

### RPi2
- Runs ntfy server on :8080
- Broker between reCamera Mosquitto and Jetson HTTP stream

### Arduino R4
- 8x12 LED matrix display
- Shows detection count
- Watchdog: displays warn frame if heartbeat missed 2x interval
- UDP listener on :8888, magic bytes b"HUMM"

### NUC
- Development machine
- Frame review via rsync from Jetson
