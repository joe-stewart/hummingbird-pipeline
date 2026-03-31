# Devices

### Upstream
- pfSense: LAN ${SUBNET_LAN}, OPT1 ${SUBNET_OPT1}
- DHCP pool: .200–245 on each subnet

### LAN (${SUBNET_LAN})
| Host   | IP           | Notes  |
|--------|--------------|--------|
| m4     | ${M4_IP}     | Static |
| nuc    | ${NUC_IP}     | Static |

### OPT1 (${SUBNET_OPT1}) — Lab
| Host       | IP            | MAC               | Notes                       |
|------------|---------------|-------------------|-----------------------------|
| beryl      | ${BERYL_IP}    |                   | OpenWrt AP, static          |
| switch-1   | ${SWITCH_IP}   |                   | Managed switch, static      |
| jetson     | ${JETSON_IP}   |                   | Static                      |
| rpi2       | ${RPI2_IP}     |                   | Static                      |
| arduino-r4 | ${ARDUINO_IP}  |                   | Static                      |
| recamera   | ${RECAMERA_IP} | a8:e2:91:2e:99:5b | wlan0 static; eth0 dynamic  |

## NUC Storage
- Samsung 980 1TB in Sabrent enclosure
- Mounted: /mnt/samsung
- Driver: UAS, USB 3.2 Gen 2, 875 MB/s write / 1.1 GB/s read

## Arduino R4
- UDP listener: ${ARDUINO_IP}:8888, magic bytes b"HUMM"
- Heartbeat interval: 5 min, watchdog fires at 2x missed
- Warn frame: hexagon with 45° slash
- Feature complete
