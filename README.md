# hummingbird-pipeline

CV-based hummingbird detection and frame capture pipeline.

## Devices
- **reCamera** (${RECAMERA_IP}) - sensor + inference (OV5647, sscma-node)
- **Jetson** (${JETSON_IP}) - orchestration + frame capture
- **Arduino R4** (${ARDUINO_IP}) - LED matrix + heartbeat watchdog
- **RPi2** (${RPI2_IP}) - ntfy broker
- **Beryl** (${BERYL_IP}) - Wifi AP
- **NUC** (${NUC_IP}) - frame viewing + development

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

## Quick Start
```bash
bash scaffold.sh
cd hummingbird-pipeline
git init && git add . && git commit -m "initial structure"
```

## Docs
- [Architecture](docs/architecture.md)
- [Decisions](docs/decisions.md)
- [Devices](docs/devices.md)
- [Models](docs/models.md)
