# Devices

See [Architecture](architecture.md) for system overview and component roles.

## Arduino R4
- UDP listener port 8888, magic bytes `b"HUMM"`
- Heartbeat interval: 5 min, watchdog fires at 2x missed
- Warn frame: hexagon with 45° slash
- Feature complete
