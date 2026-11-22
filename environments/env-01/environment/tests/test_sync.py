"""Shipped unit suite for the backfill toolchain. Passes on the shipped tree and must keep
passing after the ticket is done (`python -m pytest /app/tests`)."""
import os
import tempfile

import pytest

from ingest import IngestService, RateLimited, BATCH_MAX
from sync.source import normalise, pages


def test_normalise_canonicalises_id_and_tags():
    out = normalise({"id": 42, "value": 1, "tags": [" eu ", "eu", "", "us"]})
    assert out["id"] == "42"
    assert out["tags"] == ["eu", "us"]           # trimmed, de-duped, sorted


def test_pages_splits_into_consecutive_chunks():
    got = list(pages(list(range(1250)), 500))
    assert [len(p) for p in got] == [500, 500, 250]


def test_pages_rejects_zero_size():
    with pytest.raises(ValueError):
        list(pages([1, 2, 3], 0))


def test_service_accepts_one_and_stores_it():
    with tempfile.TemporaryDirectory() as d:
        svc = IngestService(os.path.join(d, "store"))
        svc.one({"id": "a-1", "value": 7})
        assert "a-1" in svc.ingested_ids()


def test_batch_rejects_over_max():
    with tempfile.TemporaryDirectory() as d:
        svc = IngestService(os.path.join(d, "store"))
        with pytest.raises(ValueError):
            svc.batch([{"id": str(i)} for i in range(BATCH_MAX + 1)])


def test_quota_refuses_once_burst_is_spent():
    with tempfile.TemporaryDirectory() as d:
        svc = IngestService(os.path.join(d, "store"))
        # The burst allowance is 50; the 51st back-to-back call has no token.
        refused = 0
        for i in range(120):
            try:
                svc.one({"id": f"q-{i}"})
            except RateLimited:
                refused += 1
        assert refused > 0
