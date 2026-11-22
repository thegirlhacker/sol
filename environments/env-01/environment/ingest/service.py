"""Local stand-in for the Metrics Ingest API.

The real service lives off-box; in this environment it is a process-local service backed by a
store directory so its state is durable and inspectable. It is the SDK the backfill job talks
to -- `one()` ingests a single record, `batch()` ingests a page of them.

The service enforces the published quota (see docs/api-limits.md): a token bucket of
``RATE`` requests per second. A call that arrives with no token left is refused with
``RateLimited`` -- the on-the-wire 429. Every call, accepted or refused, is appended to the
access log, so what the service received survives the run on disk.

Nothing here sleeps or blocks: a client that outruns the quota gets 429s, it is not throttled
for it. Pacing (or paging) is the caller's job -- exactly as it would be against the real API.
"""
import json
import os
import threading
import time

RATE = 50.0          # tokens per second (docs/api-limits.md: "at most 50 requests/second")
CAPACITY = 50        # burst ceiling
BATCH_MAX = 500      # docs/batch-api.md: up to 500 records per batch call

# One lock per store path, shared across threads in the process (the backfill fans out with
# threads, so the shared service must be concurrency-safe).
_LOCKS: dict[str, threading.Lock] = {}
_LOCKS_GUARD = threading.Lock()


class RateLimited(Exception):
    """Raised when a call exceeds the quota -- the service's 429."""


class IngestError(ValueError):
    pass


def _lock_for(store: str) -> threading.Lock:
    with _LOCKS_GUARD:
        return _LOCKS.setdefault(os.path.abspath(store), threading.Lock())


class IngestService:
    def __init__(self, store: str):
        self.store = store
        os.makedirs(store, exist_ok=True)
        self._lock = _lock_for(store)
        self._bucket = os.path.join(store, "bucket.json")
        self._records = os.path.join(store, "records.ndjson")
        self._access = os.path.join(store, "access.log")

    # -- quota -------------------------------------------------------------
    def _take_token(self, now: float) -> bool:
        """Refill by elapsed wall time, then spend one token. Caller holds the lock."""
        try:
            with open(self._bucket, encoding="utf-8") as fh:
                state = json.load(fh)
            tokens, last = float(state["tokens"]), float(state["last"])
        except (OSError, ValueError, KeyError):
            tokens, last = float(CAPACITY), now
        tokens = min(CAPACITY, tokens + (now - last) * RATE)
        granted = tokens >= 1.0
        if granted:
            tokens -= 1.0
        with open(self._bucket, "w", encoding="utf-8") as fh:
            json.dump({"tokens": tokens, "last": now}, fh)
        return granted

    def _log(self, endpoint: str, count: int, status: int) -> None:
        line = json.dumps({"t": time.time(), "endpoint": endpoint,
                           "count": count, "status": status})
        with open(self._access, "a", encoding="utf-8") as fh:
            fh.write(line + "\n")

    # -- endpoints ---------------------------------------------------------
    def one(self, record: dict) -> None:
        """Ingest a single record. One request, one token."""
        if not isinstance(record, dict) or "id" not in record:
            raise IngestError("record must be a dict with an 'id'")
        with self._lock:
            now = time.time()
            if not self._take_token(now):
                self._log("one", 1, 429)
                raise RateLimited("quota exceeded")
            with open(self._records, "a", encoding="utf-8") as fh:
                fh.write(json.dumps(record, sort_keys=True) + "\n")
            self._log("one", 1, 200)

    def batch(self, records: list) -> int:
        """Ingest up to BATCH_MAX records. One request, one token, many records."""
        records = list(records)
        if len(records) > BATCH_MAX:
            raise IngestError(f"batch exceeds {BATCH_MAX} records")
        if not all(isinstance(r, dict) and "id" in r for r in records):
            raise IngestError("every record must be a dict with an 'id'")
        with self._lock:
            now = time.time()
            if not self._take_token(now):
                self._log("batch", len(records), 429)
                raise RateLimited("quota exceeded")
            with open(self._records, "a", encoding="utf-8") as fh:
                for r in records:
                    fh.write(json.dumps(r, sort_keys=True) + "\n")
            self._log("batch", len(records), 200)
        return len(records)

    # -- read side (used by the task check) --------------------------------
    def ingested_ids(self) -> set:
        ids = set()
        try:
            with open(self._records, encoding="utf-8") as fh:
                for line in fh:
                    line = line.strip()
                    if line:
                        ids.add(json.loads(line)["id"])
        except (OSError, ValueError, KeyError):
            pass
        return ids
