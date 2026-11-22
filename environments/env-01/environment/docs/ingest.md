# Metrics Ingest API

The ingest API accepts analytics records from internal jobs. Two endpoints:

- `one(record)` — ingest a single record. One request.
- `batch(records)` — ingest a page of records in a single request. See `batch-api.md`.

Every job talks to it through the `ingest` client SDK (`sync/client.py`). The service keeps the
records it accepted and an access log of every request under its store directory
(`config.json: store`).

Records are normalised before they are shipped (`sync/source.normalise`): a string `id` and a
sorted, de-duplicated `tags` list.
