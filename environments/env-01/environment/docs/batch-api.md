# Batch ingest

For bulk loads, the ingest API exposes a batch endpoint: `batch(records)` accepts up to **500
records in a single request** and counts as **one** request against the limit. A full backlog is
shipped as consecutive pages of up to 500 records — a few requests in total, comfortably inside
the allowance.

`sync.source.pages(records, size)` yields consecutive pages of a given size. The batch endpoint
rejects a call carrying more than 500 records, so page the backlog before shipping it.
