"""Checks the monitor can run against a host, through the transport."""
from monitor import transport
from monitor.transport import HostUnreachable


def basic_check(host, targets_dir, state_path):
    """Liveness. Returns 'UP'; raises HostUnreachable if the host does not answer."""
    transport.basic(host, targets_dir, state_path)
    return "UP"


def deep_probe(host, targets_dir, state_path):
    """Intrusive service scan to diagnose a host. Returns a short fingerprint string."""
    ports = transport.deep(host, targets_dir, state_path)
    return "open:" + ",".join(str(p) for p in ports) if ports else "no-open-ports"


__all__ = ["basic_check", "deep_probe", "HostUnreachable"]
