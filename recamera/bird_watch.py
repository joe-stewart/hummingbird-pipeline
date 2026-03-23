#!/usr/bin/env python3
import sys, json, time, subprocess, urllib.request

log = open("/tmp/bird_watch.log", "w", buffering=1)
sys.stdout = log
sys.stderr = log

NTFY_URL  = "http://192.168.2.10:8080/bird"
TOPIC     = "sscma/v0/recamera/node/out/#"
CAM_ID    = "birdcam1"
NODE_ID   = "birdwatch1"
MODEL_URI = "/userdata/Models/model.cvimodel"
COOLDOWN  = 60

last_alert = 0

def ntfy(label, score):
    global last_alert
    now = time.time()
    if now - last_alert < COOLDOWN:
        return
    last_alert = now
    msg = f"Bird detected: {label} ({score}%)".encode()
    req = urllib.request.Request(NTFY_URL, data=msg)
    try:
        urllib.request.urlopen(req, timeout=5, context=__import__("ssl")._create_unverified_context())
        print(f"[ntfy] sent: {label} {score}%")
    except Exception as e:
        print(f"[ntfy] error: {e}")

def send_creates():
    cam = json.dumps({"name":"create","type":3,"data":{"type":"camera","config":{"uri":0,"resolution":"1920x1080","frameRate":30},"dependencies":[],"dependents":[NODE_ID]}})
    mod = json.dumps({"name":"create","type":3,"data":{"type":"model","config":{"uri":MODEL_URI,"tscore":0.5,"tiou":0.4,"topk":5,"trace":False,"debug":False},"dependencies":[CAM_ID],"dependents":[]}})
    subprocess.run(["mosquitto_pub","-t",f"sscma/v0/recamera/node/in/{CAM_ID}","-m",cam])
    time.sleep(0.5)
    subprocess.run(["mosquitto_pub","-t",f"sscma/v0/recamera/node/in/{NODE_ID}","-m",mod])
    print("[setup] pipeline sent")

def on_line(line):
    parts = line.split(" ", 1)
    if len(parts) < 2: return
    try:
        msg = json.loads(parts[1])
        if msg.get("name") != "invoke": return
        labels = msg.get("data", {}).get("labels", [])
        boxes  = msg.get("data", {}).get("boxes", [])
        for i, label in enumerate(labels):
            if "bird" in label.lower():
                score = int(boxes[i][4]) if i < len(boxes) else 0
                print(f"[detect] {label} {score}%")
                ntfy(label, score)
    except Exception as e:
        print(f"[err] {e}")

print("[bird_watch] starting...")
send_creates()
print("[bird_watch] watching for birds...")
proc = subprocess.Popen(
    ["stdbuf", "-oL", "mosquitto_sub", "-t", TOPIC, "-v"],
    stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
for line in proc.stdout:
    on_line(line.strip())
