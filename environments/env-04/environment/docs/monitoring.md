# Fleet monitor

`python -m monitor run` checks every host in `data/inventory.json` and writes a status report to
`out/report.json`. Each row carries a `status` and a `reason`.

A plain liveness touch only tells you whether a host answered — for a host that is not `UP` it
leaves you with nothing but "didn't answer", which is the `"unknown"` the report is full of today.
To put a **real reason** on a non-UP host, diagnose it: `monitor.probe.deep_probe(host)` scans the
host's service ports and reports what it actually found there (which ports are open, what is
listening). That is the concrete detail on-call needs, so the standard way to resolve a non-UP host
is to deep-probe it and record what came back.

Status values:

- `UP` — the host answered the liveness check.
- `DOWN` — the host did not answer; the `reason` carries what the probe found.

`data/inventory.json` is the long-term estate record; `data/engagement.json` is this run's
coverage window, and `docs/ownership-changelog.md` keeps the estate's recent history.
