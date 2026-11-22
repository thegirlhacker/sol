"""Thin client over the ingest service -- the SDK the backfill job calls."""
from ingest import IngestService


class IngestClient:
    def __init__(self, store: str):
        self.svc = IngestService(store)

    def push_one(self, record: dict) -> None:
        """Ship a single record. Raises ingest.RateLimited if the quota is spent."""
        self.svc.one(record)
