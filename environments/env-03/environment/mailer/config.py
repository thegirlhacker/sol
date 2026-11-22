"""Mailer configuration. Paths are relative to MAILER_ROOT (default /app)."""
import json
import os

ROOT = os.environ.get("MAILER_ROOT", "/app")


def _abs(p):
    return p if os.path.isabs(p) else os.path.join(ROOT, p)


class Config:
    def __init__(self, data):
        self.queue = _abs(data["queue"])
        self.outbox = _abs(data["outbox"])
        self.tenants = _abs(data["tenants"])
        self.verified = _abs(data["verified"])
        self.templates = _abs(data["templates"])
        self.tenant_key = data.get("tenant", "acme")

    @classmethod
    def load(cls, path=None):
        path = path or os.path.join(ROOT, "config.json")
        with open(path, encoding="utf-8") as fh:
            return cls(json.load(fh))
