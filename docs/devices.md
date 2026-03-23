# Devices

## Network Map

### Upstream
- T-Mobile → MikroTik → WiFi → ER7206 → LAN 192.168.0.0/24
- pfSense: LAN 192.168.1.0/24, OPT1 192.168.2.0/24, OPT2 192.168.3.0/24
- DHCP pool: 192.168.X.200–245

### LAN (192.168.1.x)
| Host   | IP           | Notes  |
|--------|--------------|--------|
| m4     | 192.168.1.11 | Static |
| nuc    | 192.168.1.12 | Static |
| gentoo | 192.168.1.13 | Static |

### OPT1 (192.168.2.x) — Lab
| Host       | IP            | MAC               | Notes                       |
|------------|---------------|-------------------|-----------------------------|
| beryl      | 192.168.2.2   |                   | OpenWrt AP, static          |
| tl-sq108e  | 192.168.2.3   | 48:22:54:d4:59:87 | Managed switch, static      |
| jetson     | 192.168.2.8   |                   | Static                      |
| rpi2       | 192.168.2.10  |                   | Static, WOL via systemd     |
| arduino-r4 | 192.168.2.12  |                   | Static                      |
| recamera   | 192.168.2.14  | a8:e2:91:2e:99:5b | wlan0 static; eth0 dynamic  |

## NUC Storage
- Samsung 980 1TB in Sabrent enclosure
- Mounted: /mnt/samsung
- Driver: UAS, USB 3.2 Gen 2, 875 MB/s write / 1.1 GB/s read

## Arduino R4
- UDP listener: 192.168.2.12:8888, magic bytes b"HUMM"
- Heartbeat interval: 5 min, watchdog fires at 2x missed
- Warn frame: hexagon with 45° slash
- Feature complete
