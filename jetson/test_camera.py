#!/usr/bin/env python3
"""
test_camera.py — reCamera health check
Run on Jetson via: /opt/cv-env/bin/python3 /opt/hummingbird/test_camera.py
Or from NUC via:   bash nuc/test_camera.sh

Checks:
  1. reCamera reachable (ping)
  2. sscma-node running (SSH)
  3. bird_watch.py running (SSH)
  4. WebSocket on :8090 responding and sending frames
  5. ntfy reachable from Jetson
"""

import asyncio
import json
import socket
import subprocess
import sys
import urllib.request

RECAMERA_IP   = "192.168.2.14"
RECAMERA_WS   = f"ws://{RECAMERA_IP}:8090"
RECAMERA_USER = "recamera"
NTFY_URL      = "http://192.168.2.10:8080/bird/json"
TIMEOUT       = 10  # seconds

PASS = "\033[92m✓\033[0m"
FAIL = "\033[91m✗\033[0m"
WARN = "\033[93m!\033[0m"

results = []

def report(label, ok, detail=""):
    symbol = PASS if ok else FAIL
    line = f"  {symbol} {label}"
    if detail:
        line += f" — {detail}"
    print(line)
    results.append(ok)

# ── 1. Ping ──────────────────────────────────────────────────────────────────
print("\n[1] reCamera reachability")
try:
    r = subprocess.run(["ping", "-c", "1", "-W", "2", RECAMERA_IP],
                       capture_output=True, timeout=5)
    report("ping 192.168.2.14", r.returncode == 0)
except Exception as e:
    report("ping 192.168.2.14", False, str(e))

# ── 2. sscma-node running ────────────────────────────────────────────────────
print("\n[2] sscma-node process")
try:
    r = subprocess.run(
            ["ssh", "-o", "ConnectTimeout=5", "recamera", "ps | grep sscma-node | grep -v grep"],
#        ["ssh", "-o", "IdentitiesOnly=yes", "-o", "ConnectTimeout=5",
#         f"{RECAMERA_USER}@{RECAMERA_IP}", "pgrep -f sscma-node"],
        capture_output=True, text=True, timeout=10)
    running = r.returncode == 0
    report("sscma-node", running, f"pid {r.stdout.strip()}" if running else "not found")
except Exception as e:
    report("sscma-node", False, str(e))

# ── 3. bird_watch.py running ─────────────────────────────────────────────────
print("\n[3] bird_watch.py process")
try:
    r = subprocess.run(
            ["ssh", "-o", "ConnectTimeout=5", "recamera", "ps | grep bird_watch | grep -v grep"],
        #["ssh", "-o", "IdentitiesOnly=yes", "-o", "ConnectTimeout=5",
        # f"{RECAMERA_USER}@{RECAMERA_IP}", "pgrep -f bird_watch"],
        capture_output=True, text=True, timeout=10)
    running = r.returncode == 0
    report("bird_watch.py", running, f"pid {r.stdout.strip()}" if running else "not found")
except Exception as e:
    report("bird_watch.py", False, str(e))

# ── 4. WebSocket stream ──────────────────────────────────────────────────────
print("\n[4] WebSocket stream :8090")
async def test_ws():
    try:
        import websockets
        async with websockets.connect(RECAMERA_WS, open_timeout=TIMEOUT) as ws:
            ws.ping_interval = None
            data = await asyncio.wait_for(ws.recv(), timeout=TIMEOUT)
            msg  = json.loads(data)
            keys = list(msg.keys())
            has_image = bool(msg.get("data", {}).get("image"))
            report("WebSocket connect", True)
            report("frame received", True, f"keys: {keys}")
            report("image data present", has_image)
    except Exception as e:
        report("WebSocket", False, str(e))

asyncio.run(test_ws())

# ── 5. ntfy reachable ────────────────────────────────────────────────────────
print("\n[5] ntfy broker (RPi2)")
try:
    req = urllib.request.Request(NTFY_URL)
    req.add_header("Accept", "application/json")
    # just check we can open the stream, don't wait for a message
    with urllib.request.urlopen(req, timeout=5) as r:
        report("ntfy 192.168.2.10:8080/bird", r.status == 200, f"HTTP {r.status}")
except Exception as e:
    report("ntfy 192.168.2.10:8080/bird", False, str(e))

# ── Summary ──────────────────────────────────────────────────────────────────
print()
passed = sum(results)
total  = len(results)
if passed == total:
    print(f"  \033[92mAll {total} checks passed — camera ready\033[0m")
else:
    print(f"  \033[91m{passed}/{total} checks passed\033[0m")
print()
sys.exit(0 if passed == total else 1)
