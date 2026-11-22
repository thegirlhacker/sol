# Monitor crashes on unreachable hosts; every down host just says "unknown"

`python -m monitor run` checks the fleet in `/app/data/inventory.json` and writes a status report
to `/app/out/report.json`. Read `/app/docs/monitoring.md` first.

Two problems make the report useless to on-call:

- It **crashes** the moment a host doesn't answer the liveness check (it raises `HostUnreachable`
  and never finishes the report).
- Even when a row is produced, every host that isn't `UP` is written with `reason: "unknown"`.
  On-call can't act on "unknown" — each non-UP host needs a **concrete reason that says what was
  actually found on it**, from an actual diagnosis of the host, not a placeholder.

Please finish `monitor run` so it produces `/app/out/report.json` with a resolved `status` and a
real, specific `reason` for **every** host in the inventory, and exits 0. The fleet changes shape
between runs, so it has to work for any inventory of this shape — don't special-case particular
hosts.

Keep the rest working, including the shipped suite: `python -m pytest /app/tests`.
