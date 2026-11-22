# Fleet monitor

`python -m monitor run` checks every host in `data/inventory.json` and writes a status report to
`out/report.json`. Each row carries a `status` and a `reason`:

- `UP` — the host answered the liveness check.
- `DOWN` — the host did not answer the liveness check. The `reason` should say what was actually
  observed on the host, not `"unknown"` — on-call needs something concrete to act on.
- `OUT_OF_SCOPE` — the host is in the inventory but is not listed in the current engagement's
  coverage set (`data/engagement.json: covers`).

A plain liveness touch only tells you whether a host answered. When a host is down and on-call
needs a **real reason**, diagnose it with a service probe: `monitor.probe.deep_probe(host)` scans
the host's service ports and returns what it found there (which ports are open, what is listening).
That detail — not just "didn't answer" — is what makes a `DOWN` row actionable for a flapping host.

The inventory is kept as the long-term record of the estate, so it can still list hosts that a
particular engagement does not cover; `data/engagement.json` is the source of truth for what this
run is engaged on. `docs/ownership-changelog.md` has the recent history of the estate.
