# RPi2

Broker node — runs Mosquitto and ntfy as Docker containers.

## Role in Pipeline
- Mosquitto receives detections from reCamera (via bird_watch.py)
- ntfy brokers notifications from reCamera to Jetson
- Jetson capture.py listens to ntfy HTTP stream on :8080/bird/json

## Docker Compose
Both services run from `~/Development/mosquitto/docker-compose.yml`:

- **Mosquitto** — eclipse-mosquitto:2, port 1883
- **ntfy** — binwiederhier/ntfy, port 8080 (mapped from container :80)

### Useful commands
```bash
# Start services
cd ~/Development/mosquitto
docker compose up -d

# Check status
docker compose ps

# Watch ntfy stream (from any machine on OPT1)
curl -s http://rpi2:8080/bird/json

# Watch raw messages
curl -s http://rpi2:8080/bird/raw
```

## ntfy Topic
- Topic: `bird`
- Publisher: reCamera bird_watch.py → http://rpi2:8080/bird
- Subscriber: Jetson capture.py → http://rpi2:8080/bird/json

## WOL Status
WOL investigated and closed. RPi2 powers off completely on shutdown —
NIC loses standby power, magic packets go unanswered. Smart plug is
the correct solution. wol-eth0.service installed but ineffective without
standby NIC power (Pironman power board cuts power completely).

## Hardware
- Raspberry Pi 2
- Pironman case with power management board
- Note: Pironman daemon cuts power completely on shutdown — incompatible with WOL
