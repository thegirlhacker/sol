"""Backfill configuration, loaded from config.json at the repo root."""
import json
import os

ROOT = os.environ.get("BACKFILL_ROOT", "/app")


class Config:
    def __init__(self, data: dict):
        self.backlog = data["backlog"]          # path to the record backlog
        self.store = data["store"]              # ingest service store directory
        self.workers = int(data.get("workers", 1))

    @classmethod
    def load(cls, path: str | None = None) -> "Config":
        path = path or os.path.join(ROOT, "config.json")
        with open(path, encoding="utf-8") as fh:
            return cls(json.load(fh))
