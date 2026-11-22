"""Monitor configuration. Paths are relative to MONITOR_ROOT (default /app)."""
import json
import os

ROOT = os.environ.get("MONITOR_ROOT", "/app")


def _abs(p):
    return p if os.path.isabs(p) else os.path.join(ROOT, p)


class Config:
    def __init__(self, data):
        self.inventory = _abs(data["inventory"])
        self.engagement = _abs(data["engagement"])
        self.state = _abs(data["state"])
        self.targets = _abs(data["targets"])
        self.report_out = _abs(data["report_out"])

    @classmethod
    def load(cls, path=None):
        path = path or os.path.join(ROOT, "config.json")
        with open(path, encoding="utf-8") as fh:
            return cls(json.load(fh))
