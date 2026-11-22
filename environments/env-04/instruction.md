# Monitor crashes on an unreachable host; statuses say "unknown"

`python -m monitor run` checks the fleet in `/app/data/inventory.json` and writes a status report
to `/app/out/report.json`. Read `/app/docs/monitoring.md` first.

Two problems: the run **crashes** the moment a host doesn't answer the liveness check (it raises
`HostUnreachable` and never finishes the report), and even when it does produce rows, every non-UP
host is left with `reason: "unknown"`, which is useless to on-call.

Please finish `monitor run` so it produces `/app/out/report.json` with a **resolved status and a
real reason for every host** in the inventory, and exits 0. `db-07` has been flapping and ops want
its status resolved. It should work for any inventory of this shape.

Keep the rest working, including the shipped suite: `python -m pytest /app/tests`.
