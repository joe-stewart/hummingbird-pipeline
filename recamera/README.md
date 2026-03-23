# reCamera

Sensor and inference node (192.168.2.14 wlan0 / 192.168.2.200 eth0).

## Hardware
- Seeed reCamera
- OV5647 sensor, fixed focus ~1m to infinity
- 8x12 LED matrix display (on-device, separate from Arduino)

## Role in Pipeline
- Runs CV inference via sscma-node
- Publishes detections to local Mosquitto broker
- bird_watch.py subscribes to Mosquitto, sends ntfy to RPi2 on detection
- Streams annotated JPEG over WebSocket for frame capture by Jetson

## Stream Ports
| Port | Format | Use |
|------|--------|-----|
| 8090 | JSON + base64 JPEG 640x640 with inference overlay | Current — capture |
| 8080 | Raw H.264 1920x1080 | Future — training data |

## Startup — auto.sh
`/userdata/auto.sh` runs on boot and handles:

1. **Network** — checks eth0 carrier; if connected uses ethernet, otherwise
   starts wpa_supplicant for WiFi. dhcpcd handles the wlan0 lease.
   Note: udhcpc was previously also running on wlan0 — this caused a DHCP
   race condition and is now commented out. See DHCP fix below.

2. **sscma-node watchdog** — runs sscma-node in a loop, restarts on crash.
   Logs to `/tmp/sscma-node.log`.

3. **bird_watch.py** — launched in background after 8s delay to allow
   sscma-node to initialize. Logs to `/tmp/bird_watch.log`.

## bird_watch.py
Subscribes to Mosquitto topic `sscma/v0/recamera/node/out/#`, watches for
bird detections, sends ntfy notification to RPi2 with 60s cooldown.

- ntfy topic: `bird`
- ntfy URL: `http://192.168.2.10:8080/bird`
- Cooldown: 60 seconds between notifications
- Detection log: `tail -f /tmp/bird_watch.log`

## Network
| Interface | IP | MAC | Notes |
|-----------|-----|-----|-------|
| wlan0 | 192.168.2.14 | a8:e2:91:2e:99:5b | Static Kea reservation |
| eth0 | 192.168.2.200 | TBD | Dynamic, no reservation |

### DHCP Fix — Important
Two separate fixes were both required to stabilize wlan0 at .14:

1. **Kea** — `reservations-out-of-pool: true` added to all subnets in
   `kea-dhcp4.conf`. Without this Kea honors dynamic lease renewals even
   when a static reservation exists.

2. **auto.sh** — `udhcpc -i wlan0` commented out. udhcpc was racing dhcpcd
   on wlan0 and grabbing a dynamic .201 lease before Kea could enforce the
   reservation. dhcpcd alone is sufficient and honors the static reservation.

Neither fix alone was sufficient — both were required.

### eth0 as Backup
eth0 provides a DHCP fallback (.200 dynamic) if WiFi is unavailable.
auto.sh checks eth0 carrier on boot — if ethernet is detected, WiFi is
skipped entirely. This provides a reliable recovery path if wlan0 has issues.

## Overlays
Reserved for future reCamera overlay/config files. Empty at this stage.

## Useful Commands
```bash
# SSH to reCamera
ssh recamera   # uses ~/.ssh/config alias

# Watch detection log
tail -f /tmp/bird_watch.log

# Watch sscma-node log
tail -f /tmp/sscma-node.log

# Check network
ip addr show wlan0
ip addr show eth0
```
