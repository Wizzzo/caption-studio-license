#!/usr/bin/env python3
"""Validate status.yaml. The app fails CLOSED on any parse error, so a bad push here
would disable every installed copy of the app. CI must stop that before it merges."""
import re
import sys

import yaml

VERSION = re.compile(r"^v\d+\.\d+\.\d+$")

try:
    with open("status.yaml", encoding="utf-8") as f:
        data = yaml.safe_load(f)
except yaml.YAMLError as e:
    sys.exit(f"status.yaml does not parse: {e}")

errors = []
if not isinstance(data, dict):
    sys.exit("status.yaml must be a mapping")

latest = data.get("latest_version")
if not isinstance(latest, str) or not VERSION.match(latest):
    errors.append(f"latest_version must look like v1.2.3, got {latest!r}")

for key, value in data.items():
    if key == "latest_version":
        continue
    if not isinstance(key, str) or not VERSION.match(key):
        errors.append(f"unexpected key {key!r} (expected vX.Y.Z or latest_version)")
    elif not isinstance(value, dict) or not isinstance(value.get("enabled"), bool):
        errors.append(f"{key}: needs 'enabled: true|false' (a boolean, not a string)")

if isinstance(latest, str) and latest in data and data[latest].get("enabled") is not True:
    errors.append(f"latest_version {latest} is not enabled; is that intentional? Users would be told to update to a disabled build")
if isinstance(latest, str) and latest not in data:
    errors.append(f"latest_version {latest} has no entry, so it would run disabled (fail closed)")

if errors:
    print("\n".join(errors))
    sys.exit(1)
enabled = sorted(k for k, v in data.items() if isinstance(v, dict) and v.get("enabled") is True)
print(f"ok: latest {latest}; enabled: {', '.join(enabled)}")
