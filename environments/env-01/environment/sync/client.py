"""Thin client over the ingest service -- the SDK the backfill job calls.

`push_one` ships and works. `push_batch` is wired to the batch endpoint but was left
half-finished: it forwards the whole list in a single call, so it raises on any backlog larger
than one page. docs/batch-api.md describes how the endpoint is meant to be driven.
"""
from ingest import IngestService, BATCH_MAX


class IngestClient:
    def __init__(self, store: str):
        self.svc = IngestService(store)

    def push_one(self, record: dict) -> None:
        """Ship a single record. Raises ingest.RateLimited if the quota is spent."""
        self.svc.one(record)

    def push_batch(self, records: list) -> int:
        """Ship a page of records in one request.

        TODO(backfill): this still hands the whole backlog to the endpoint in one call, which
        the service rejects past %d records. See docs/batch-api.md.
        """ % BATCH_MAX
        return self.svc.batch(records)
