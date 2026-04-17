#!/bin/bash
# Collect reCamera SoC temperature and write to file for Prometheus exporter
TEMP=$(ssh recamera 'cat /sys/class/thermal/thermal_zone0/temp' 2>/dev/null)
if [ $? -eq 0 ] && [ -n "$TEMP" ]; then
    echo "$TEMP" > /tmp/recamera_temp
else
    echo "collect_temp: SSH to recamera failed" >&2
fi
