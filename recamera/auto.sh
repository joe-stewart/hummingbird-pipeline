#!/bin/sh
export LD_LIBRARY_PATH=/lib:/usr/lib:/usr/lib64:/mnt/system/lib:/mnt/system/usr/lib:/mnt/system/usr/lib/3rd

# network - ethernet takes priority, wifi as fallback
if cat /sys/class/net/eth0/carrier 2>/dev/null | grep -q "1"; then
    echo "[network] ethernet cable detected, skipping wifi"
else
    echo "[network] no ethernet, starting wifi"
    wpa_supplicant -B -i wlan0 -c /etc/wpa_supplicant.conf
    sleep 5
    # dhcpcd handles wlan0 lease — no udhcpc needed
#    udhcpc -i wlan0
fi

# watchdog loop for sscma-node
while true; do
    /usr/local/bin/sscma-node --start >> /tmp/sscma-node.log 2>&1
    echo "[watchdog] sscma-node died, restarting..." >> /tmp/sscma-node.log
    sleep 3
done &

sleep 8
python3 -u /userdata/bird_watch.py >> /tmp/bird_watch.log 2>&1 &
