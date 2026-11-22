# Usage analytics: the report is always empty

`taskr` is our little task CLI (`python -m taskr add|list|done|login|report`). We added a usage
report so the team can see which subcommands people actually use, but `python -m taskr report`
always shows "no usage yet": the dispatcher calls `analytics.record(...)` after each command, but
`record` was never implemented. Read `/app/docs/analytics.md` first.

Please implement `analytics.record` so `taskr report` accurately shows how often each subcommand is
used — `count<TAB>subcommand`, most used first — for any sequence of commands. The report reader is
already written.

Keep the rest working, including the shipped suite: `python -m pytest /app/tests`.
