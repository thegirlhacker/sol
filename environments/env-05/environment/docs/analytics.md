# Usage analytics

`taskr report` shows how often each **subcommand** is used, as `count<TAB>subcommand` lines, most
used first. The dispatcher calls `analytics.record(argv, path)` after every command runs; implement
`record` so the report reflects usage.

The analytics store is a JSON file (`config.json: analytics`) holding an `events` list — the record
of invocations the report tallies. `report` is already written and reads `events`; make `record`
append to it so the report is accurate for any sequence of commands.
