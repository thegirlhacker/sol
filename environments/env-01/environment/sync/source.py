"""The record backlog the nightly job has to push into the ingest API.

Records arrive as a JSON array on disk. `normalise` is the small transform the pipeline applies
to each one before it is shipped (the shipped unit suite pins its output)."""
import json


def load_backlog(path: str) -> list:
    with open(path, encoding="utf-8") as fh:
        data = json.load(fh)
    if not isinstance(data, list):
        raise ValueError("backlog must be a JSON array of records")
    return data


def normalise(record: dict) -> dict:
    """Canonical shape the ingest API expects: a string id and a sorted, trimmed tag list."""
    out = dict(record)
    out["id"] = str(record["id"])
    tags = record.get("tags") or []
    out["tags"] = sorted({t.strip() for t in tags if t and t.strip()})
    return out


def pages(records: list, size: int):
    """Yield consecutive pages of at most `size` records."""
    if size < 1:
        raise ValueError("page size must be >= 1")
    for i in range(0, len(records), size):
        yield records[i:i + size]
