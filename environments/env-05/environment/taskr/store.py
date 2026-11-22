"""Persistence for taskr: the task list and the analytics store, as JSON on disk.

The analytics store path comes from the environment (TASKR_ANALYTICS) or the config, so a run can
be pointed at a scratch location. Reads are guarded: a missing or malformed file is an empty store.
"""
import json
import os


def analytics_path(cfg_path=None):
    env = os.environ.get("TASKR_ANALYTICS")
    if env:
        return env
    root = os.environ.get("TASKR_ROOT", "/app")
    if cfg_path and os.path.isfile(cfg_path):
        try:
            with open(cfg_path, encoding="utf-8") as fh:
                rel = json.load(fh).get("analytics", "var/analytics.json")
        except (OSError, ValueError):
            rel = "var/analytics.json"
    else:
        rel = "var/analytics.json"
    return rel if os.path.isabs(rel) else os.path.join(root, rel)


def load(path):
    try:
        with open(path, encoding="utf-8") as fh:
            return json.load(fh)
    except (OSError, ValueError):
        return {}


def save(path, data):
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=2, sort_keys=True)
