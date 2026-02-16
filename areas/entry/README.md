# Entry Area

The main entry/foyer of TheLodge. Contains four Aqara ceiling lights (Matter), a Zooz Z-Wave switch, two Zooz Z-Wave remotes, and a Fibaro motion sensor.

---

## Light Groups

### `light.entry_light_group` — Entry Light Group

HA group containing all four ceiling lights. Useful for bulk on/off control, but individual lights must be addressed directly for specific brightness, color temp, or RGB settings due to differing color mode capabilities.

| Member Entity | Color Mode | Capabilities |
|---|---|---|
| `light.entry_ceiling_north` | `color_temp` | 2702K–6535K (warm to daylight) |
| `light.entry_ceiling_north_2` | `hs` | Full RGB via `rgb_color`, no color temp |
| `light.entry_ceiling_south` | `color_temp` | 2702K–6535K (warm to daylight) |
| `light.entry_ceiling_south_2` | `hs` | Full RGB via `rgb_color`, no color temp |

> **Important:** The `_2` entities are the RGB channel of the same physical fixture. Each Aqara ceiling light exposes two HA entities — one for white/color temp, one for HS color.

---

## Lights

### Entry Ceiling North

| Property | Value |
|---|---|
| **Device** | Aqara Colorful Ceiling Light 36W |
| **Protocol** | Matter |
| **Manufacturer** | Aqara |
| **Serial** | 54ef441000c0a6cd |
| **Firmware** | v26 |
| **Area** | Entry |

| Entity ID | Color Mode | Temp Range | Notes |
|---|---|---|---|
| `light.entry_ceiling_north` | `color_temp` | 2702K–6535K | White channel. Use `brightness` (0–255) and `color_temp_kelvin`. `brightness_pct` is unreliable. |
| `light.entry_ceiling_north_2` | `hs` | N/A | RGB channel. Use `rgb_color` for stable solid colors. `hs_color` can cause color cycling/pulsing. Set `effect: "none"` to prevent unwanted effects. |

### Entry Ceiling South

| Property | Value |
|---|---|
| **Device** | Aqara Colorful Ceiling Light 36W |
| **Protocol** | Matter |
| **Manufacturer** | Aqara |
| **Serial** | 54ef441000cbd63e |
| **Firmware** | v26 |
| **Area** | Entry |

| Entity ID | Color Mode | Temp Range | Notes |
|---|---|---|---|
| `light.entry_ceiling_south` | `color_temp` | 2702K–6535K | White channel. Same behavior as North. |
| `light.entry_ceiling_south_2` | `hs` | N/A | RGB channel. Same behavior as North_2. |

### Aqara Light Gotchas

- **`brightness_pct` is unreliable** — always use `brightness` (0–255 scale) for consistent results
- **`hs_color` causes pulsing/cycling** on the HS-mode entities — use `rgb_color` instead for solid colors
- **`effect: "none"`** should be set when using RGB to prevent unwanted color cycling
- Each physical fixture exposes **two entities** (white channel + RGB channel) via Matter

---

## Switches

### Entry Main — `switch.entry_main_2`

| Property | Value |
|---|---|
| **Device** | Zooz ZEN71 (On/Off Switch) |
| **Protocol** | Z-Wave |
| **Manufacturer** | Zooz |
| **Firmware** | v3.70.0 |
| **Z-Wave Node** | 267 |
| **Area** | Entry |
| **Smart Switch Mode** | Local and Z-Wave control disabled |

**Entities:**

| Entity ID | Type | Description |
|---|---|---|
| `switch.entry_main_2` | switch | Primary on/off control |
| `event.entry_main_scene_001_2` | event | Scene 001 (paddle up) |
| `event.entry_main_scene_002_2` | event | Scene 002 (paddle down) |
| `event.entry_main_scene_003_2` | event | Scene 003 |
| `select.entry_main_scene_control_2` | select | Scene control enable/disable |
| `select.entry_main_smart_switch_mode_2` | select | Smart switch mode config |
| `sensor.entry_main_node_status_2` | sensor | Z-Wave node status |
| `update.entry_main_firmware_2` | update | Firmware update entity |
| `button.entry_main_ping_2` | button | Z-Wave ping |
| `button.entry_main_identify_2` | button | Identify device |

---

## Remotes

### Entry Remote North

| Property | Value |
|---|---|
| **Device** | Zooz ZEN34 (Remote Switch) |
| **Protocol** | Z-Wave (battery) |
| **Manufacturer** | Zooz |
| **Firmware** | v2.0.2 |
| **Z-Wave Node** | 268 |
| **Area** | Entry |

**Entities:**

| Entity ID | Type | Description |
|---|---|---|
| `event.entry_remote_north_scene_001` | event | Scene 001 (button press) |
| `event.entry_remote_north_scene_002` | event | Scene 002 (button press) |
| `sensor.entry_remote_north_battery_level` | sensor | Battery level (%) |
| `sensor.entry_remote_north_node_status` | sensor | Z-Wave node status |
| `update.entry_remote_north_firmware` | update | Firmware update entity |
| `button.entry_remote_north_ping` | button | Z-Wave ping |
| `button.entry_remote_north_identify` | button | Identify device |

### Entry Remote South

| Property | Value |
|---|---|
| **Device** | Zooz ZEN34 (Remote Switch) |
| **Protocol** | Z-Wave (battery) |
| **Manufacturer** | Zooz |
| **Firmware** | v2.0.2 |
| **Z-Wave Node** | 271 |
| **Area** | Entry |

**Entities:**

| Entity ID | Type | Description |
|---|---|---|
| `event.entry_remote_south_scene_001` | event | Scene 001 (button press) |
| `event.entry_remote_south_scene_002` | event | Scene 002 (button press) |
| `sensor.entry_remote_south_battery_level` | sensor | Battery level (%) |
| `sensor.entry_remote_south_node_status` | sensor | Z-Wave node status |
| `update.entry_remote_south_firmware` | update | Firmware update entity |
| `button.entry_remote_south_ping` | button | Z-Wave ping |
| `button.entry_remote_south_identify` | button | Identify device |

---

## Sensors

### Entry Motion — Fibaro FGMS001

| Property | Value |
|---|---|
| **Device** | Fibaro FGMS001 (Motion Sensor) |
| **Protocol** | Z-Wave (battery) |
| **Manufacturer** | Fibargroup |
| **Firmware** | v3.3 |
| **Z-Wave Node** | 11 |
| **Area** | Entry |

**Entities:**

| Entity ID | Type | Description |
|---|---|---|
| `binary_sensor.entry_motion_motion_detection` | binary_sensor | Motion detected (on/off) |
| `sensor.entry_motion_air_temperature` | sensor | Temperature (°F) |
| `sensor.entry_motion_illuminance` | sensor | Light level (lx) |
| `sensor.entry_motion_seismic_intensity` | sensor | Vibration/seismic intensity |
| `sensor.entry_motion_acceleration_x_axis` | sensor | Accelerometer X (m/s²) |
| `sensor.entry_motion_acceleration_y_axis` | sensor | Accelerometer Y (m/s²) |
| `sensor.entry_motion_acceleration_z_axis` | sensor | Accelerometer Z (m/s²) |
| `binary_sensor.entry_motion_tampering_product_cover_removed` | binary_sensor | Tamper detection |
| `sensor.entry_motion_battery_level` | sensor | Battery level (%) |
| `sensor.entry_motion_node_status` | sensor | Z-Wave node status |
| `update.entry_motion_firmware` | update | Firmware update entity |
| `button.entry_motion_ping` | button | Z-Wave ping |

---

## Other Devices

### Entry Tablet

| Entity ID | Type | Description |
|---|---|---|
| `device_tracker.2605_4a80_2101_cf31_656c_15d5_e8e3_56f4_dynamic_midco_net` | device_tracker | Tablet presence |
| `binary_sensor.entry_tablet_connectivity` | binary_sensor | Network connectivity |
| `switch.entry_tablet_do_not_disturb` | switch | DND toggle |

### Entry Door (Ring)

| Entity ID | Type | Description |
|---|---|---|
| `device_tracker.ring_entry_door` | device_tracker | Ring doorbell presence |
| `binary_sensor.side_door_ding` | binary_sensor | Doorbell ding event |

---

## Automations

### Entry Motion Automation

Motion-triggered staggered lighting for the entry area. Each ceiling light turns on with independent brightness, color, and timeout settings, creating a gradual fade-out effect as lights shut off one by one.

See [`automations/entry_motion.yaml`](automations/entry_motion.yaml) for the full configuration.

**Trigger:** `binary_sensor.entry_motion_motion_detection` → `on`
**Condition:** After sunset / before sunrise
**Mode:** `restart` (re-trigger resets all timers)

| Light | Brightness | Color | Timeout |
|---|---|---|---|
| `entry_ceiling_north` | 75% (191/255) | 2702K warm white | 2 min |
| `entry_ceiling_north_2` | 100% (255/255) | Blue (rgb 0,0,255) | 5 min |
| `entry_ceiling_south` | 100% (255/255) | 6535K daylight | 10 min |
| `entry_ceiling_south_2` | 100% (255/255) | Blue (rgb 0,0,255) | 15 min |
