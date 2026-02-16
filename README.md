# TheLodge Home Assistant Automations

A collection of Home Assistant automation packages powering **TheLodge** — a home lab network built on Unraid with extensive IoT integration, multi-zone audio, and smart home controls.

## Architecture Overview

TheLodge runs Home Assistant in a Docker container on Unraid, using the [packages](https://www.home-assistant.io/docs/configuration/packages/) pattern to keep automations modular and self-contained. Each package bundles its own REST commands, timers, helpers, and automations in a single YAML file.

### Infrastructure

| Component | Details |
|---|---|
| **Server** | Unraid (10.0.101.3) |
| **Home Assistant** | Docker container |
| **Audio System** | Jukebox Server (Docker, 10.0.101.52) → WiiM Ultra (LinkPlay, 10.0.102.31) → HTD Lync 12 multi-zone amp |
| **Networking** | Macvlan (br0) for container isolation, AdGuard DNS, Nginx Proxy Manager |
| **IoT** | Zigbee2MQTT, Z-Wave, WiFi switches/sensors, Matter |

## Areas

Area-based documentation for all entities, groups, devices, and automations organized by room/zone.

| Area | Devices | Automations | Description |
|---|---|---|---|
| [Entry](areas/entry/) | 4 lights, 1 switch, 2 remotes, 1 motion sensor | Entry Motion | Staggered motion-triggered lighting with Aqara Matter lights, Zooz Z-Wave switches |

## Package Categories

### 🔊 Media & Audio

Automations involving the Jukebox server, WiiM Ultra, HTD Lync amp zones, and speaker control.

| Package | Description |
|---|---|
| [shower_music.yaml](packages/media/shower_music.yaml) | Master bathroom shower music system with multi-zone muting and timed shutoff |

### 💡 Lighting

| Package | Description |
|---|---|
| [entry_motion.yaml](areas/entry/automations/entry_motion.yaml) | Staggered entry lighting on motion detection with per-light brightness, color, and timeout |

### 🌡️ Climate

*Coming soon* — HeatMaster SS Pro wood boiler monitoring, HVAC automations, and temperature-based controls.

### 🏠 Presence & Scenes

*Coming soon* — Arrival/departure routines, occupancy-based automations, and multi-room scene coordination.

---

## Installation

1. Copy the desired package YAML file into your Home Assistant `config/packages/` directory
2. Ensure `packages` is enabled in `configuration.yaml`:
   ```yaml
   homeassistant:
     packages: !include_dir_named packages
   ```
3. Adjust entity IDs, IP addresses, and zone names to match your setup
4. Restart Home Assistant to load the new package

## Notes

- **Aqara Matter Lights**: Each fixture exposes two HA entities — one for white/color temp (`color_temp` mode) and one for RGB (`hs` mode). Use `brightness` (0–255) instead of `brightness_pct`, and `rgb_color` instead of `hs_color` for stable solid colors.
- **WiiM REST API**: These packages communicate with WiiM devices via the LinkPlay HTTP API (`/httpapi.asp`). Your WiiM device must be accessible on your network.
- **Jukebox Server**: A custom Docker container running nginx that serves MP3 files and M3U playlists. Audio is downloaded via yt-dlp in a companion container.
- **HTD Lync Zones**: Controlled through Home Assistant `media_player` entities via the Juke integration.

## License

MIT — use whatever is helpful for your own setup.
