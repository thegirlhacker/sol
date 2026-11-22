# Metrics Ingest API

The ingest API accepts analytics records from internal jobs. Jobs talk to it through the `ingest`
client SDK (`sync/client.py`): `push_one(record)` ships a single record, one request.

The service keeps the records it accepted (`records.ndjson`) and an access log of every request
(`access.log`) under its store directory (`config.json: store`), so what it received survives the
run on disk.

Records are normalised before they are shipped (`sync/source.normalise`): a string `id` and a
sorted, de-duplicated `tags` list.

See `api-limits.md` for the request quota.
