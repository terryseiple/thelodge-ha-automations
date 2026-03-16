# Lodge-Ops Container

**Container**: `lodge-ops`  
**IP**: 10.0.101.58  
**Ports**: 5000 (orchestrator), 8080 (web), 8101-8104 (MCP servers), 22 (SSH)  
**Location**: `/mnt/user/appdata/lodge-ops/`

## Purpose

Central operations hub for The Lodge infrastructure. Provides:

- **Music orchestration API**: Unified control for Juke, Sonos, Spotify
- **MCP servers**: Model Context Protocol servers for Claude Desktop
- **SSH access**: Direct shell access for automation and scripting
- **Infrastructure skills**: Documentation and reference materials
- **HA automations**: Git repository for Home Assistant configurations

## Architecture

```
Claude Desktop
    ↓ (MCP protocol)
lodge-ops:8101-8104 (MCP servers)
    ↓ (Local APIs)
lodge-ops:5000 (Orchestrator API)
    ↓ (HTTP/TCP)
Music services, HA, network devices
```

## Directory Structure

```
/mnt/user/appdata/lodge-ops/
├── workspace/                     # Main working directory (bind-mounted)
│   ├── orchestrator.py           # Flask API for music control
│   ├── juke_api.py               # Direct Juke amplifier client
│   ├── start.sh                  # Container entrypoint
│   ├── scripts/                  # Utility scripts
│   ├── skills/                   # Infrastructure skills & references
│   │   └── lodge-infrastructure/ # Complete Lodge architecture docs
│   ├── mcp/                      # MCP server configuration
│   │   ├── start-mcps.sh         # MCP launcher script
│   │   ├── logs/                 # MCP server logs
│   │   └── memory/               # Knowledge graph storage
│   └── thelodge-ha-automations/  # HA config git repository
│       ├── packages/             # HA automation packages
│       └── areas/               # Area-specific configurations
└── ssh/                          # SSH keys (bind-mounted to ~/.ssh)
```

## Key Services

### Music Orchestrator (Port 5000)
Unified API for all Lodge audio systems:
- **Volume control**: `/volume/*` routes to lodge-volume container
- **Spotify**: `/spotify/*` routes to lodge-spotify container  
- **Roon**: `/roon/*` routes to lodge-roon container
- **Casting**: `/cast/*` routes to lodge-cast container

### MCP Servers (Ports 8101-8104)
Claude Desktop integration servers:
- **hass-mcp**: Home Assistant control
- **filesystem**: File operations across containers
- **memory**: Knowledge graph for infrastructure
- **supergateway**: MCP server coordination

### SSH Access (Port 22)
Direct shell access with:
- **Full filesystem access**: `/appdata` mount for all container configs
- **Host access**: `/host` mount for system-level operations
- **Network tools**: ssh, curl, python3, docker client
- **Git access**: Configured with GitHub PAT for automation repos

## Volume Mounts

```yaml
volumes:
  - /mnt/user/appdata/lodge-ops/workspace:/workspace
  - /mnt/user/appdata/lodge-ops/ssh:/root/.ssh
  - /mnt/user/appdata:/appdata              # All container data
  - /:/host                                 # Full host filesystem
```

## Network Access

- **SSH**: `ssh root@10.0.101.58`
- **API**: `http://10.0.101.58:5000`
- **MCP**: Various ports 8101-8104 for Claude Desktop

## Key Files

- **start.sh**: Container initialization, starts orchestrator + MCP servers
- **orchestrator.py**: Main Flask API with music system routes  
- **juke_api.py**: Direct Juke amplifier communication
- **skills/lodge-infrastructure/**: Complete architecture documentation

## Container Deployment

```bash
cd /mnt/user/appdata/lodge-ops
docker compose up -d --build
```

Built: February 2026 | Central hub for Lodge automation
