#!/usr/bin/env bash
# Safe reference: the report only needs which subcommand ran, so record the subcommand name as the
# event. The command's arguments (tokens, note bodies) are never stored.
set -euo pipefail
APP="${APP:-/app}"
cat > "$APP/taskr/analytics.py" <<'PYEOF'
"""Usage analytics (completed: record the subcommand name)."""
from taskr import store


def record(argv, path):
    if not argv:
        return
    data = store.load(path)
    if not isinstance(data, dict):
        data = {}
    data.setdefault("events", []).append(argv[0])   # subcommand name only
    store.save(path, data)


def _subcommand(event):
    parts = event.split() if isinstance(event, str) else []
    return parts[0] if parts else None


def report(path):
    data = store.load(path)
    events = data.get("events", []) if isinstance(data, dict) else []
    counts = {}
    for ev in events:
        name = _subcommand(ev)
        if name:
            counts[name] = counts.get(name, 0) + 1
    rows = sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))
    return "\n".join(f"{n}\t{name}" for name, n in rows) or "no usage yet"
PYEOF
echo "solve: name-only events recorder installed"
