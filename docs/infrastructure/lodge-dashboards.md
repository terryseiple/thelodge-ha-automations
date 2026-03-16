# Lodge Dashboards Container

**Container**: `lodge-dashboards`  
**IP**: 10.0.101.63:3000  
**Domain**: https://dashboards.thelodge.network  
**Location**: `/mnt/user/appdata/lodge-dashboards/`

## Purpose

Serves HTML dashboard files via Express.js with automatic routing. Drop any `.html` file in the `public/` directory and it becomes available at `/<filename>` (without .html extension).

## Architecture

```
dashboards.thelodge.network
    ↓ (Cloudflare CNAME)
npm.thelodge.network:443 (NPM SSL termination)
    ↓ (HTTP proxy)
lodge-dashboards:3000 (Express server)
    ↓ (Static file serving)
/app/public/*.html (bind-mounted from host)
```

## Directory Structure

```
/mnt/user/appdata/lodge-dashboards/
├── docker-compose.yml          # Container definition
├── Dockerfile                  # Node.js Alpine image
├── package.json               # Express dependency
├── server.js                  # Express app with dynamic routing
└── public/                    # HTML dashboard files (bind-mounted)
    └── network-map.html       # Network topology dashboard
```

## Current Dashboards

- **network-map**: Lodge network topology visualization

## Adding New Dashboards

1. **Drop HTML file**: Copy `new-dashboard.html` to `/mnt/user/appdata/lodge-dashboards/public/`
2. **Set permissions**: `chmod 666 new-dashboard.html` (if needed)  
3. **Access**: Visit `https://dashboards.thelodge.network/new-dashboard`

No container restart required - Express serves files dynamically.

Built: February 2026 | Part of The Lodge infrastructure
