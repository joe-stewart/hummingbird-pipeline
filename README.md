# hummingbird-pipeline

CV-based hummingbird detection and frame capture pipeline.

## Devices
- **reCamera** (192.168.2.14) — sensor + inference (OV5647, sscma-node)
- **Jetson** (192.168.2.8) — orchestration + frame capture
- **Arduino R4** (192.168.2.12) — LED matrix + heartbeat watchdog
- **RPi2** (192.168.2.10) — ntfy broker
- **Beryl** (192.168.2.2) — OpenWrt AP
- **NUC** (192.168.1.12) — frame viewing + development

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
