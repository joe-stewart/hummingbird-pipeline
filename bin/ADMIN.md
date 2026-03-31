# hummingbird-pipeline

CV-based hummingbird detection and frame capture pipeline using edge AI inference
on a reCamera, orchestrated by a Jetson, with Arduino alerting and RPi notification brokering.

## Status

Data collection phase — pipeline is running and capturing frames. No trained model yet.

## Hardware

| Device | Model | Role |
|--------|-------|------|
| reCamera | Seeed reCamera 2002W (SG2002, OV5647, 64GB) | Sensor + CV inference |
| Jetson | reComputer J3011 (Orin Nano 8GB, JetPack 5.1.1) | Orchestration + frame capture |
| Arduino | R4 WiFi | LED matrix display + heartbeat watchdog |
| RPi | Raspberry Pi 5 | Mosquitto + ntfy notification broker |
| Beryl | GL.iNet Beryl (MT-1300) | WiFi access point |

> **Note on WiFi AP**: The Beryl was chosen specifically for reliable AP mode.
> The GL.iNet Opal (MT300N-V2) has known issues in AP mode that caused
> connectivity problems with the reCamera — avoid it for this use case.

## Flow

```
reCamera (sensor + inference)
    ↓
Jetson (orchestration + capture)
    ↓              ↓
  NUC           Arduino R4
(viewing)        (alerting)
    ↑
  RPi
(ntfy broker)
```

## Configuration

Network addresses and credentials are not committed to this repo.
To see all files requiring configuration:

```bash
grep -r '\${' --include="*.py" --include="*.conf" --include="*.ini" --include="*.h" . | grep -v bin/
```

## Docs

- [Architecture](docs/architecture.md)
- [Decisions](docs/decisions.md)
- [Devices](docs/devices.md)
- [Models](docs/models.md)

## Network Map

### Upstream
- pfSense: LAN ${SUBNET_LAN}, OPT1 ${SUBNET_OPT1}
- DHCP pool: .200–245 on each subnet

### LAN (${SUBNET_LAN})
| Host   | IP           | Notes  |
|--------|--------------|--------|
| m4     | ${M4_IP}     | Static |
| nuc    | ${NUC_IP}    | Static |

### OPT1 (${SUBNET_OPT1}) — Lab
| Host       | IP            | MAC               | Notes                       |
|------------|---------------|-------------------|-----------------------------|
| beryl      | ${BERYL_IP}   |                   | OpenWrt AP, static          |
| switch-1   | ${SWITCH_IP}  |                   | Managed switch, static      |
| jetson     | ${JETSON_IP}  |                   | Static                      |
| rpi2       | ${RPI2_IP}    |                   | Static                      |
| arduino-r4 | ${ARDUINO_IP} |                   | Static                      |
| recamera   | ${RECAMERA_IP}| a8:e2:91:2e:99:5b | wlan0 static; eth0 dynamic  |

## NUC Storage
- Samsung 980 1TB in Sabrent enclosure
- Mounted: /mnt/samsung
- Driver: UAS, USB 3.2 Gen 2, 875 MB/s write / 1.1 GB/s read

## Operational Decisions

### DHCP / Kea
- reservations-out-of-pool: true required on all subnets
- reCamera fix required BOTH: reservations-out-of-pool AND removing udhcpc from auto.sh
- Neither change alone was sufficient

### Buildroot
Explored but not in active use. Modding running system in place.
Not a blocker.

### WOL
Both Jetson and RPi2 go fully dark on shutdown — NIC loses standby power.
Smart plug is the correct solution. WOL investigation closed.

### SSH
IdentitiesOnly yes in ~/.ssh/config for ${SUBNET_OPT1} — prevents MaxAuthTries.

### Jetson Wheels
Do not commit .whl files. Document source and version in bin/ADMIN.md.
Wheels go stale across JetPack versions.

### hummingbird systemd user
Dedicated system user (no login, no home) for principle of least privilege.
joe added to hummingbird group for frame access.
/opt/hummingbird/frames/ at 775.

### Dev vs Production paths
- Dev: ~/Development/hummer-capture/ (Jetson, joe)
- Production: /opt/hummingbird/ (Jetson, hummingbird user)
- deploy.sh promotes dev → production

### Arduino warn frame
Bird icon impractical at 8x12 pixels. Hexagon with 45° slash chosen as
warn frame — clear and readable at that resolution.

### Repo structure
Single repo, folders per device. Frames gitignored everywhere — runtime output not source.
