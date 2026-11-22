"""The nightly backfill.

As shipped, `run` pushes the backlog one record at a time and does nothing about the quota, so
once the burst allowance is spent the next call raises and the job dies partway through -- the
bug the ticket is about. Finishing the job means pushing the whole backlog through the ingest
API without that happening.
"""
from sync.config import Config
from sync.client import IngestClient
from sync.source import load_backlog, normalise


def prepare(cfg: Config) -> list:
    """Load and normalise the backlog into the shape the API expects."""
    return [normalise(r) for r in load_backlog(cfg.backlog)]


def run(cfg: Config) -> int:
    """Push the whole backlog. Returns the number of records shipped.

    Shipped behaviour: sequential, one request per record, no quota handling. It ships the
    burst allowance and then raises ingest.RateLimited on the next call.
    """
    records = prepare(cfg)
    client = IngestClient(cfg.store)
    shipped = 0
    for record in records:
        client.push_one(record)
        shipped += 1
    return shipped
