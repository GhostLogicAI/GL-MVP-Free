# GhostLogic Free Edition

## Install
**macOS:** Run `GhostLogic-Free.pkg` → installs to `/Applications/GhostLogic-Free.app`
**Windows:** Run `GhostLogic-Free-Installer.exe` → installs to `C:\Program Files\GhostLogic Free\`

## Run
**macOS:** Open `GhostLogic-Free.app` or run `watchdog` binary
**Windows:** Start Menu → GhostLogic Watchdog

## Dashboard
Open browser: `http://localhost:4242`

## Files
Agent monitors: `watch/` directory
Events logged to: `evidence_log.jsonl`
Uploads to: Cloudflare R2 + KV (configure via environment variables)

## Environment Variables
Set: `CLOUDFLARE_ACCOUNT_ID`, `CLOUDFLARE_ACCESS_KEY`, `CLOUDFLARE_SECRET_KEY`, `CLOUDFLARE_R2_BUCKET`, `CLOUDFLARE_R2_PREFIX`, `CLOUDFLARE_KV_NAMESPACE`, `CLOUDFLARE_KV_PREFIX`
