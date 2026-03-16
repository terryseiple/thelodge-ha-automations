# Entry Area

Main entryway with motion-activated staggered lighting, dual door contact sensors, ecobee climate control, and Ring doorbell.

## Devices & Entities

### Lights

**Aqara Colorful Ceiling Light 36W** (Matter, x2)  
Each fixture exposes two light entities via Matter — one for color temperature (white channel) and one for HS color (accent channel).

| Entity ID | Mode | Range | Device |
|-----------|------|-------|--------|
| `light.entry_ceiling_north` | color_temp | 2702K–6535K | Serial: 54ef441000c0a6cd, FW: v26 |
| `light.entry_ceiling_north_accent` | hs (RGB) | Full color via `rgb_color` | Same device (accent channel) |
| `light.entry_ceiling_south` | color_temp | 2702K–6535K | Serial: 54ef441000cbd63e, FW: v26 |
| `light.entry_ceiling_south_accent` | hs (RGB) | Full color via `rgb_color` | Same device (accent channel) |

**Light Group:**
- `light.entry_light_group` — Contains all 4 ceiling light entities

> **Aqara Matter Notes:**  
> - Use `brightness` (0–255), NOT `brightness_pct`  
> - Use `rgb_color` for accent entities, NOT `hs_color` (causes pulsing)  
> - Use `color_temp_kelvin` for white entities  
> - Always set `effect: "none"` on accent entities to prevent stuck effects  
> - Accent entities are hidden by integration but fully functional

### Switches

**Zooz ZEN71 (Z-Wave, node 267)**
| Entity ID | Description |
|-----------|-------------|
| `switch.entry_main` | Primary on/off (Smart Switch Mode: local + Z-Wave disabled) |
| `event.entry_main_scene_001` | Scene event (up paddle) |
| `event.entry_main_scene_002` | Scene event (down paddle) |
| `event.entry_main_scene_003` | Scene event (config button) |
| `select.entry_main_scene_control` | Enable/disable scene events |
| `select.entry_main_smart_switch_mode` | Smart switch relay mode |
| `sensor.entry_main_node_status` | Z-Wave node alive/dead status |
| `button.entry_main_ping` | Ping Z-Wave node |
| `button.entry_main_identify` | Identify device |
| `update.entry_main_firmware` | Firmware update entity (v3.70.0) |

### Door Sensors

**Entry Garage Door Sensor** — SmartThings Multipurpose Sensor (2018, IM6001-MPP01)  
Zigbee via Zigbee2MQTT | Labels: `zigbee`, `door_sensor`
| Entity ID | Description |
|-----------|-------------|
| `binary_sensor.entry_garage_door_sensor_contact` | Door open/closed (device_class: door) |
| `binary_sensor.entry_garage_door_sensor_battery_low` | Low battery alert |
| `binary_sensor.entry_garage_door_sensor_tamper` | Tamper detection |
| `binary_sensor.entry_garage_door_sensor_moving` | Movement/vibration detection |

**Entry Side Door Sensor** — Visonic MCT-340 E  
Zigbee via Zigbee2MQTT | Labels: `zigbee`, `door_sensor`
| Entity ID | Description |
|-----------|-------------|
| `binary_sensor.entry_side_door_sensor_contact` | Door open/closed (device_class: door) |
| `binary_sensor.entry_side_door_sensor_battery_low` | Low battery alert |
| `binary_sensor.entry_side_door_sensor_tamper` | Tamper detection |

### Motion Sensor

**Fibaro FGMS001** (Z-Wave, node 11, FW: v3.3)
| Entity ID | Description |
|-----------|-------------|
| `binary_sensor.entry_motion_motion_detection` | Motion trigger (automation trigger) |
| `sensor.entry_motion_temperature` | Temperature reading |
| `sensor.entry_motion_illuminance` | Light level (lux) |
| `sensor.entry_motion_seismic_intensity` | Vibration/seismic |
| `sensor.entry_motion_air_temperature` | Air temperature |
| `sensor.entry_motion_battery_level` | Battery % |

### Remotes

**Zooz ZEN34** (Z-Wave, battery, x2)
| Device | Node | Entities |
|--------|------|----------|
| Entry Remote North | 268 | Scene events, battery, node status, FW update, ping, identify |
| Entry Remote South | 271 | Scene events, battery, node status, FW update, ping, identify |

### Climate

**ecobee ECB501** (HomeKit integration)  
Serial: 421883660639 | FW: v4.10.80256
| Entity ID | Description |
|-----------|-------------|
| `climate.entry` | HVAC control (off/heat/cool/heat_cool), 45–92°F, fan on/auto |

Built-in sensors: motion, temperature, humidity (via HomeKit)

### Other Devices

| Device | Key Entities |
|--------|--------------|
| Entry Tablet | `device_tracker`, connectivity sensor, DND switch |
| Ring Entry Door | `binary_sensor.side_door_ding`, cameras, motion, battery |

## Automations

- **[Entry Motion Automation](automations/entry_motion.yaml)** — Staggered multi-light response to motion detection (sunset–sunrise)

## Protocols

| Protocol | Devices |
|----------|---------|
| Matter | Aqara ceiling lights (x2) |
| Z-Wave | Zooz ZEN71 switch, ZEN34 remotes (x2), Fibaro motion sensor |
| Zigbee (Z2M) | SmartThings door sensor, Visonic door sensor |
| HomeKit | ecobee thermostat |
| Ring | Entry Door doorbell |
