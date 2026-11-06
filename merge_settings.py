"""Set the statusLine entry in a Claude Code settings.json, keeping every other setting.

Usage: python merge_settings.py <path/to/settings.json> "<status line command>"
"""
import json
import os
import shutil
import sys

path, command = sys.argv[1], sys.argv[2]

settings = {}
if os.path.exists(path):
    with open(path, encoding="utf-8") as f:
        text = f.read()
    if text.strip():
        try:
            settings = json.loads(text)
        except json.JSONDecodeError as e:
            sys.exit(f"{path} is not valid JSON ({e}); fix it first — nothing was changed")
    shutil.copy2(path, path + ".bak")
    print(f"backup: {path}.bak")

# refreshInterval: re-run every second so the reset countdown keeps ticking while idle
settings["statusLine"] = {"type": "command", "command": command, "refreshInterval": 1}

with open(path, "w", encoding="utf-8") as f:
    json.dump(settings, f, indent=2, ensure_ascii=False)
    f.write("\n")
print(f"statusLine -> {command}")
