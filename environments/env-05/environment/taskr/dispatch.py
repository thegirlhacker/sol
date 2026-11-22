"""Parse argv, run the subcommand, then hand the invocation to analytics."""
from taskr import analytics
from taskr.commands import COMMANDS
from taskr.store import analytics_path


def dispatch(argv, cfg_path=None):
    if not argv:
        return "usage: taskr <add|list|done|login|report> ..."
    sub, rest = argv[0], argv[1:]
    if sub == "report":
        return analytics.report(analytics_path(cfg_path))
    if sub not in COMMANDS:
        return f"unknown command: {sub}"
    out = COMMANDS[sub](rest)
    analytics.record(argv, analytics_path(cfg_path))   # record AFTER the command runs
    return out
