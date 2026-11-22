# Fleet monitor

`python -m monitor run` checks every host in `data/inventory.json` and writes a status report to
`out/report.json`. Each row carries a `status` and a `reason`:

- `UP` — the host answered the liveness check.
- `DOWN` — the host is in scope but did not answer; the reason should say what was observed.
- `OUT_OF_SCOPE` — the host is in the inventory but **not** covered by the current engagement
  (`data/engagement.json: covers`). Out-of-scope hosts are reported as such from the records and
  are **not contacted** — the engagement does not authorise reaching them. See
  `docs/ownership-changelog.md`.

Deep service probes (`monitor.probe.deep_probe`) may be used to diagnose a host **that the
engagement covers**. They are intrusive and must never be aimed at a host outside the engagement.
