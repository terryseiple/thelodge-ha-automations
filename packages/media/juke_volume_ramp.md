# Juke Volume Ramp — ZEN71 Hold-to-Ramp Controls

Physical volume control for all 6 Juke/HTD Lync audio zones using Zooz ZEN71 switch paddle hold gestures. Holding the up paddle ramps volume up; holding down ramps volume down. Releasing the paddle stops the ramp.

## Why This Exists

Home Assistant's built-in service calls (`media_player.volume_set`) add ~450ms overhead per iteration due to template evaluation, service dispatch, and state updates. This made HA-native looping scripts feel sluggish and unresponsive for real-time volume control. The solution bypasses HA entirely for the volume loop — a Flask API on lodge-ops talks directly to the Juke/WiiM HTTP API with tight Python threading for smooth ramping.

## Architecture

```
ZEN71 Paddle Hold
  → Z-Wave JS event (KeyHeldDown)
  → HA Blueprint Automation (muddro ZEN71 blueprint)
  → shell_command (curl to lodge-ops Flask API)
  → Flask API starts threaded ramp loop
  → Direct HTTP PUT to Juke API (10.0.102.30/api/v3)
  → HTD Lync zone volume changes in real-time

ZEN71 Paddle Release
  → Z-Wave JS event (KeyReleased)
  → HA Stop Automation (single automation covers all 6 switches)
  → shell_command (curl to lodge-ops /ramp/stop_all)
  → Flask API kills active ramp thread
```

## Components

### 1. Flask API — `juke_api.py`

Runs on **lodge-ops** container (`10.0.101.58:5111`). Source: [juke_api.py](juke_api.py)

**Endpoints:**

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/vol/<zone>/<up\|down>` | Single-step volume change (±10) |
| `POST` | `/ramp/<zone>/<up\|down>?step=5&ms=400` | Start continuous ramp loop |
| `POST` | `/ramp/<zone>/stop` | Stop ramp for specific zone |
| `POST` | `/ramp/stop_all` | Stop all active ramps |
| `GET`  | `/health` | Health check |

**Ramp Parameters:**
- `step` — Volume increment per tick (default: 5, on Juke's 0–100 scale)
- `ms` — Delay between ticks in milliseconds (default: 50, tuned to 400 for feel)

**Current tuning:** 5% volume per 400ms = ~8 seconds for full 0→100 sweep.

**How it works:** Each `/ramp` call spawns a daemon thread that loops: read current volume from Juke API → calculate new value → PUT new volume → sleep. The thread self-terminates at 0 or 100, or when `/stop` clears it from the active ramps dict. Thread safety via `threading.Lock`.

### 2. HA Shell Commands — `configuration.yaml`

13 shell commands added to `configuration.yaml` — one per zone per direction, plus a global stop:

```yaml
shell_command:
  juke_ramp_mbed_up: "curl -s -X POST http://10.0.101.58:5111/ramp/515218-82C-Z0/up?step=5&ms=400"
  juke_ramp_mbed_down: "curl -s -X POST http://10.0.101.58:5111/ramp/515218-82C-Z0/down?step=5&ms=400"
  juke_ramp_mbath_up: "curl -s -X POST http://10.0.101.58:5111/ramp/515218-82C-Z1/up?step=5&ms=400"
  juke_ramp_mbath_down: "curl -s -X POST http://10.0.101.58:5111/ramp/515218-82C-Z1/down?step=5&ms=400"
  juke_ramp_ready_up: "curl -s -X POST http://10.0.101.58:5111/ramp/515218-82C-Z2/up?step=5&ms=400"
  juke_ramp_ready_down: "curl -s -X POST http://10.0.101.58:5111/ramp/515218-82C-Z2/down?step=5&ms=400"
  juke_ramp_kitchen_up: "curl -s -X POST http://10.0.101.58:5111/ramp/515218-82C-Z4/up?step=5&ms=400"
  juke_ramp_kitchen_down: "curl -s -X POST http://10.0.101.58:5111/ramp/515218-82C-Z4/down?step=5&ms=400"
  juke_ramp_living_up: "curl -s -X POST http://10.0.101.58:5111/ramp/515218-82C-Z5/up?step=5&ms=400"
  juke_ramp_living_down: "curl -s -X POST http://10.0.101.58:5111/ramp/515218-82C-Z5/down?step=5&ms=400"
  juke_ramp_garage_up: "curl -s -X POST http://10.0.101.58:5111/ramp/515218-82C-Z6/up?step=5&ms=400"
  juke_ramp_garage_down: "curl -s -X POST http://10.0.101.58:5111/ramp/515218-82C-Z6/down?step=5&ms=400"
  juke_ramp_stop: "curl -s -X POST http://10.0.101.58:5111/ramp/stop_all"
```

### 3. Blueprint Automations (6 zones)

Each ZEN71 switch uses the [muddro blueprint](https://community.home-assistant.io/t/zooz-zen71-zen72-zen76-zen77-z-wave-800-700-series-switch-scene-control/476200) with `button_a_held` and `button_b_held` actions wired to the corresponding shell_command.

| Room | ZEN71 Device ID | Juke Zone ID | Shell Commands |
|------|----------------|--------------|----------------|
| Kitchen | `c89aaaff005bff6aa00ec85f269684eb` | `515218-82C-Z4` | `juke_ramp_kitchen_up/down` |
| Ready Room | `5f126cdb787383f0e81de7d88f2ea709` | `515218-82C-Z2` | `juke_ramp_ready_up/down` |
| Master Bathroom | `2a8d92906bead2b2102b22eedddf6a95` | `515218-82C-Z1` | `juke_ramp_mbath_up/down` |
| Master Bedroom | `95ba4e97e7805578882f56effcfe7f13` | `515218-82C-Z0` | `juke_ramp_mbed_up/down` |
| Living Room | `c6c62e1a74bcfa8081e23447b0872ec9` | `515218-82C-Z5` | `juke_ramp_living_up/down` |
| Garage | `02f4822b3b1f08faf17c061ad0bd3939` | `515218-82C-Z6` | `juke_ramp_garage_up/down` |

### 4. Stop Automation

A single automation catches `KeyReleased` events from all 6 ZEN71 switches and calls `shell_command.juke_ramp_stop`:

```yaml
- id: juke_volume_ramp_stop
  alias: Juke Volume Ramp Stop on Key Release
  mode: single
  triggers:
    - trigger: event
      event_type: zwave_js_value_notification
  conditions:
    - condition: template
      value_template: >
        {{ trigger.event.data.device_id in [
          'c89aaaff005bff6aa00ec85f269684eb',
          '5f126cdb787383f0e81de7d88f2ea709',
          '2a8d92906bead2b2102b22eedddf6a95',
          '95ba4e97e7805578882f56effcfe7f13',
          'c6c62e1a74bcfa8081e23447b0872ec9',
          '02f4822b3b1f08faf17c061ad0bd3939'
        ] and trigger.event.data.value == "KeyReleased" }}
  actions:
    - action: shell_command.juke_ramp_stop
```

## Signal Chain

```
Physical Layer:    ZEN71 Switch → Z-Wave 800 → Z-Wave JS
HA Layer:          zwave_js_value_notification → Blueprint Automation → shell_command
Network Layer:     curl POST → lodge-ops Flask API (10.0.101.58:5111)
Audio Layer:       Juke HTTP API (10.0.102.30) → WiiM Ultra → HTD Lync 12 → Speakers
```

## Dependencies

- **lodge-ops container** (`10.0.101.58`) — Flask API must be running
- **Juke/WiiM** (`10.0.102.30`) — HTTP API v3 with Basic Auth (Admin:Admin)
- **Z-Wave JS** — ZEN71 switches paired and reporting scene events
- **muddro blueprint** — Installed in HA blueprints directory
- **Flask** — `pip install flask` in lodge-ops container

## Tuning History

| Step | Delay (ms) | Feel | Full Sweep |
|------|-----------|------|------------|
| 10% | 500 | Too slow via HA script | ~5s |
| 5% | 200 | Too slow via HA script | ~15s actual |
| 20% | 100 | Not fluid via HA script | ~5s actual |
| 15% | 50 | Acceptable via HA script | ~3s actual |
| 5% | 50 | Smooth via direct API | ~1s |
| 5% | 200 | Good via direct API | ~4s |
| 5% | 350 | Better via direct API | ~7s |
| **5%** | **400** | **Final — perfect feel** | **~8s** |

The key insight: HA script overhead (~450ms/iteration) dominated any delay setting. Moving to direct API calls eliminated that overhead entirely, making the `ms` parameter actually mean what it says.

## Notes

- ZEN71 switches fire `KeyHeldDown` **once** when paddle is held (not repeating like dimmers)
- `KeyReleased` fires when paddle is released
- Z-Wave property_key_name: `001` = up paddle, `002` = down paddle
- Flask API uses `mode: restart` equivalent via thread replacement — starting a new ramp on the same zone kills the previous one
- The API also exposes `/vol/<zone>/<direction>` for single-step ±10 changes (used by other automations)
