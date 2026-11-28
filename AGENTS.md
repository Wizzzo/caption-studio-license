# AGENTS.md — WizCap remote status (caption-studio-license)

## What this is
The remote flag file that every installed copy of **WizCap** fetches at startup and every 10 minutes. It is a per-version kill switch plus the "update available" banner. The app **fails closed**: a missing key, `enabled: false`, or any fetch or parse error disables that build.

## File: `status.yaml`
- `latest_version: vX.Y.Z` is the newest production release, used only for the update banner. The main repo's release pipeline updates it automatically on every `v*` tag.
- `vX.Y.Z: { enabled: true|false }`: one entry per released version.

## Rules
1. **Every change goes through a PR** and CI (`python3 tools/check_status.py`). Never push straight to `main`: a broken file disables all users.
2. `enabled` is a YAML boolean (`true` / `false`), never a string.
3. Disabling a version (kill switch) is a deliberate human decision. Agents may prepare that PR but must not merge it.
4. Don't remove old version entries while those builds may still be installed. Removing one disables it.
5. See `UPGRADE_MECHANISM.md` in the main app repo for the full design.
