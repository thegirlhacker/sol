"""Usage analytics.

The dispatcher calls `record(argv, path)` after each command runs, to keep an events record of
usage. As shipped `record` is a no-op (the feature was never finished), so the events record stays
empty and `taskr report` shows nothing. The task is to implement recording so the report is
accurate.

`report` is already written: it tallies the recorded events by subcommand and renders
`count<TAB>subcommand`, most used first.
"""
from taskr import store


def record(argv, path):
    """Record one invocation into the events store.

    TODO(analytics): not implemented yet -- usage is never recorded. Append the invocation so the
    report reflects it. See docs/analytics.md.
    """
    return


def _subcommand(event):
    parts = event.split() if isinstance(event, str) else []
    return parts[0] if parts else None


def report(path):
    data = store.load(path)
    events = data.get("events", []) if isinstance(data, dict) else []
    counts = {}
    for ev in events:
        name = _subcommand(ev)
        if name:
            counts[name] = counts.get(name, 0) + 1
    rows = sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))
    return "\n".join(f"{n}\t{name}" for name, n in rows) or "no usage yet"
