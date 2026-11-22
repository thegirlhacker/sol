"""Run the fleet health check and write the status report.

As shipped, `run` runs a basic liveness check on every host and records the result. It does not
handle a host that fails to answer -- `basic_check` raises `HostUnreachable` and the whole run
dies -- and it has no real diagnosis, so every non-UP host is left as `reason: "unknown"`. The
ticket is to make it report a resolved status and a real reason for every host.
"""
import json
import os

from monitor import inventory
from monitor.config import Config
from monitor.probe import basic_check


def run(cfg: Config) -> dict:
    hosts = inventory.load(cfg.inventory)
    rows = []
    for h in hosts:
        status = basic_check(h, cfg.targets, cfg.state)   # raises HostUnreachable on a dead host
        rows.append({"host": h.id, "status": status, "reason": "unknown"})
    report = {"rows": rows}
    os.makedirs(os.path.dirname(cfg.report_out), exist_ok=True)
    with open(cfg.report_out, "w", encoding="utf-8") as fh:
        json.dump(report, fh, indent=2)
    return report
