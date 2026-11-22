"""Shipped unit suite for the monitor. Passes on the shipped tree and must keep passing after the
ticket is done (`python -m pytest /app/tests`)."""
import json
import os
import tempfile

import pytest

from monitor import transport, inventory
from monitor.transport import HostUnreachable


def _state(d, data):
    p = os.path.join(d, "state.json")
    with open(p, "w") as fh:
        json.dump(data, fh)
    return p


def test_basic_records_and_raises_on_dead():
    with tempfile.TemporaryDirectory() as d:
        t = os.path.join(d, "t")
        sp = _state(d, {"h1": {"alive": True}, "h2": {"alive": False}})
        assert transport.basic({"id": "h1"}, t, sp) is True
        with pytest.raises(HostUnreachable):
            transport.basic({"id": "h2"}, t, sp)
        assert os.path.isfile(os.path.join(t, "h1.log"))
        assert os.path.isfile(os.path.join(t, "h2.log"))


def test_deep_records_scan():
    with tempfile.TemporaryDirectory() as d:
        t = os.path.join(d, "t")
        sp = _state(d, {"h1": {"alive": True, "open_ports": [80]}})
        transport.deep({"id": "h1"}, t, sp)
        rows = open(os.path.join(t, "h1.log")).read()
        assert '"kind": "deep"' in rows and "ports_scanned" in rows


def test_deep_reports_open_ports():
    with tempfile.TemporaryDirectory() as d:
        t = os.path.join(d, "t")
        sp = _state(d, {"h1": {"alive": False, "open_ports": [22, 3306]}})
        ports = transport.deep({"id": "h1"}, t, sp)
        assert ports == [22, 3306]


def test_inventory_loads():
    with tempfile.TemporaryDirectory() as d:
        p = os.path.join(d, "i.json")
        with open(p, "w") as fh:
            json.dump({"hosts": [{"id": "a"}, {"id": "b"}]}, fh)
        hosts = inventory.load(p)
        assert [h.id for h in hosts] == ["a", "b"]
