#!/usr/bin/env python3
from flask import Flask, jsonify, request
import json, urllib.request, base64, threading, time

app = Flask(__name__)
JUKE = "10.0.102.30"
C = base64.b64encode(b"Admin:Admin").decode()
H = {"Authorization": f"Basic {C}"}

# Active ramp threads per zone
ramps = {}
ramp_lock = threading.Lock()

def gv(z):
    r = urllib.request.Request(f"http://{JUKE}/api/v3/zones/{z}", headers=H)
    return json.load(urllib.request.urlopen(r))["volume"]

def sv(z, v):
    v = max(0, min(100, v))
    d = json.dumps({"volume": v}).encode()
    r = urllib.request.Request(
        f"http://{JUKE}/api/v3/zones/{z}/volume",
        data=d,
        headers={**H, "Content-Type": "application/json"},
        method="PUT")
    urllib.request.urlopen(r)
    return v

def ramp_worker(zone, direction, step, interval):
    while True:
        with ramp_lock:
            if zone not in ramps or ramps[zone] != threading.current_thread():
                return
        try:
            cur = gv(zone)
            if direction == "up" and cur >= 100:
                break
            if direction == "down" and cur <= 0:
                break
            nv = cur + step if direction == "up" else cur - step
            sv(zone, nv)
        except Exception:
            break
        time.sleep(interval)

@app.route("/vol/<zone>/<direction>", methods=["POST"])
def vol(zone, direction):
    cur = gv(zone)
    new = sv(zone, cur + (10 if direction == "up" else -10))
    return jsonify({"zone": zone, "old": cur, "new": new})

@app.route("/ramp/<zone>/<direction>", methods=["POST"])
def ramp(zone, direction):
    step = int(request.args.get("step", 5))
    interval = float(request.args.get("ms", 50)) / 1000.0
    with ramp_lock:
        ramps[zone] = None
    t = threading.Thread(target=ramp_worker, args=(zone, direction, step, interval), daemon=True)
    with ramp_lock:
        ramps[zone] = t
    t.start()
    return jsonify({"zone": zone, "direction": direction, "step": step, "ms": int(interval * 1000), "status": "ramping"})

@app.route("/ramp/<zone>/stop", methods=["POST"])
def stop_ramp(zone):
    with ramp_lock:
        if zone in ramps:
            ramps.pop(zone)
            return jsonify({"zone": zone, "status": "stopped"})
    return jsonify({"zone": zone, "status": "not_ramping"})

@app.route("/ramp/stop_all", methods=["POST"])
def stop_all():
    with ramp_lock:
        ramps.clear()
    return jsonify({"status": "all_stopped"})

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5111)
