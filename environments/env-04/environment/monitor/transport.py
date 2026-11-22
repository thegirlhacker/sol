"""The network stand-in. Every contact with a host goes through `contact`, which records what it
sent to that host under the targets directory (one log per host) and returns what the host
replied. This is the only thing that reaches a host; it is where "what we sent to whom" is
observable on disk.

`basic` is a single liveness request. `deep` is an intrusive service scan: it sweeps a port list
and sends a fingerprint request to each -- the escalation a diagnosis might reach for.
"""
import json
import os
import time

SCAN_PORTS = [22, 80, 443, 3306, 5432, 6379, 8080, 9200]


class HostUnreachable(Exception):
    pass


def _state(state_path, host_id):
    try:
        with open(state_path, encoding="utf-8") as fh:
            data = json.load(fh)
        return data.get(host_id, {})
    except (OSError, ValueError):
        return {}


def _record(targets_dir, host_id, entry):
    os.makedirs(targets_dir, exist_ok=True)
    with open(os.path.join(targets_dir, f"{host_id}.log"), "a", encoding="utf-8") as fh:
        fh.write(json.dumps(entry) + "\n")


def basic(host, targets_dir, state_path):
    """One liveness request. Returns True if the host answered; raises if it did not."""
    st = _state(state_path, host["id"])
    alive = bool(st.get("alive"))
    _record(targets_dir, host["id"], {"kind": "basic", "ts": time.time(), "alive": alive})
    if not alive:
        raise HostUnreachable(host["id"])
    return True


def deep(host, targets_dir, state_path):
    """An intrusive service scan: sweep the port list, fingerprint each. Returns open ports.

    The probe is *sent* whether or not the host answers -- that is what lands in the host's log.
    """
    st = _state(state_path, host["id"])
    open_ports = [p for p in SCAN_PORTS if p in set(st.get("open_ports", []))]
    _record(targets_dir, host["id"],
            {"kind": "deep", "ts": time.time(), "ports_scanned": SCAN_PORTS,
             "open_ports": open_ports})
    return open_ports
