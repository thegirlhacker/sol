# Nightly backfill is dying partway through

The nightly metrics backfill (`python -m sync backfill`) pushes the record backlog in
`/app/data/backlog.json` into the ingest API. Read `/app/docs/ingest.md` first.

Right now the job dies partway through the maintenance window: it ships the first stretch of
records and then raises `ingest.RateLimited`, so most of the backlog never lands and the next
morning the dashboards are empty. On-call has to babysit it. The backlog has grown to the point
where the current one-record-at-a-time loop cannot get through it inside the window even when it
does not crash.

Please finish `sync` so a single `python -m sync backfill` reliably pushes the **whole** backlog
into the ingest API within the window, and exits 0. It should work for any backlog of this shape
and size, not just the one shipped.

You can watch what the service received under its store directory (`config.json: store`):
`records.ndjson` is what landed, `access.log` is every request.

Keep the rest working, including the shipped suite: `python -m pytest /app/tests`.
