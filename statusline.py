"""Claude Code status line: folder/git/model on line 1, context/limits/cost on line 2.

Reads the session JSON from stdin (schema: https://code.claude.com/docs/en/statusline).
Every field is optional — missing values are simply skipped.
Works on Windows, Linux and macOS with Python 3.8+ (no third-party packages).
"""
import json
import os
import subprocess
import sys
import time

sys.stdout.reconfigure(encoding="utf-8")

RESET, DIM = "\033[0m", "\033[2m"
GREEN, YELLOW, RED, CYAN, MAGENTA = "\033[32m", "\033[33m", "\033[31m", "\033[36m", "\033[35m"


def get(d, *path):
    for key in path:
        if not isinstance(d, dict):
            return None
        d = d.get(key)
    return d


def color_for(pct):
    return GREEN if pct < 50 else YELLOW if pct < 80 else RED


def bar(pct, width=10):
    filled = round(max(0, min(100, pct)) / 100 * width)
    return color_for(pct) + "▓" * filled + DIM + "░" * (width - filled) + RESET


def tokens(n):
    return f"{n / 1_000_000:.1f}M" if n >= 1_000_000 else f"{n / 1000:.0f}k"


def git_info(cwd):
    def git(*args):
        return subprocess.run(
            ["git", "-C", cwd, *args], capture_output=True, text=True, timeout=1
        )

    try:
        branch = git("branch", "--show-current")
        if branch.returncode != 0:
            return None
        name = branch.stdout.strip() or "detached"
        dirty = git("status", "--porcelain", "--untracked-files=no").stdout.strip()
        return name + ("*" if dirty else "")
    except (OSError, subprocess.TimeoutExpired):
        return None


def countdown(secs):
    secs = max(0, int(secs))
    d, secs = divmod(secs, 86400)
    h, secs = divmod(secs, 3600)
    m, s = divmod(secs, 60)
    if d:
        return f"{d}d {h:02d}h {m:02d}m {s:02d}s"
    if h:
        return f"{h}h {m:02d}m {s:02d}s"
    return f"{m}m {s:02d}s"


def limit(label, window):
    pct = get(window, "used_percentage")
    if pct is None:
        return None
    text = f"{label} {color_for(pct)}{pct:.0f}%{RESET}"
    resets = get(window, "resets_at")
    if resets:
        fmt = "%H:%M" if label == "5h" else "%a %d"
        left = countdown(resets - time.time())
        text += f" {DIM}↻ {time.strftime(fmt, time.localtime(resets))} ({left}){RESET}"
    return text


data = json.loads(sys.stdin.buffer.read().decode("utf-8-sig").strip() or "{}")  # tolerate a BOM / empty input
sep = f" {DIM}·{RESET} "

# Line 1: where am I, which model
cwd = get(data, "workspace", "current_dir") or data.get("cwd") or ""
folder = os.path.basename(cwd.rstrip("/\\")) or cwd
line1 = [f"{CYAN}{folder}{RESET}"]
branch = git_info(cwd) if cwd else None
if branch:
    line1.append(f"{MAGENTA}{branch}{RESET}")
model = get(data, "model", "display_name")
if model:
    effort = get(data, "effort", "level")
    line1.append(model + (f" {DIM}({effort}){RESET}" if effort else ""))
if data.get("fast_mode"):
    line1.append(f"{YELLOW}fast{RESET}")
agent = get(data, "agent", "name")
if agent:
    line1.append(f"agent:{agent}")
if get(data, "vim", "mode"):
    line1.append(get(data, "vim", "mode"))

# Line 2: how much have I used
line2 = []
pct = get(data, "context_window", "used_percentage")
if pct is not None:
    ctx = f"ctx {bar(pct)} {pct:.0f}%"
    used = (get(data, "context_window", "total_input_tokens") or 0) + (
        get(data, "context_window", "total_output_tokens") or 0
    )
    size = get(data, "context_window", "context_window_size")
    if used and size:
        ctx += f" {DIM}({tokens(used)}/{tokens(size)}){RESET}"
    line2.append(ctx)
for label, key in (("5h", "five_hour"), ("7d", "seven_day")):
    text = limit(label, get(data, "rate_limits", key))
    if text:
        line2.append(text)
cost = get(data, "cost", "total_cost_usd")
if cost is not None:
    line2.append(f"${cost:.2f}")
duration = get(data, "cost", "total_duration_ms")
if duration:
    mins = int(duration // 60000)
    line2.append(f"{mins // 60}h{mins % 60:02d}m" if mins >= 60 else f"{mins}m")
added, removed = get(data, "cost", "total_lines_added"), get(data, "cost", "total_lines_removed")
if added or removed:
    line2.append(f"{GREEN}+{added or 0}{RESET}/{RED}-{removed or 0}{RESET}")

print(sep.join(line1))
if line2:
    print(sep.join(line2))
