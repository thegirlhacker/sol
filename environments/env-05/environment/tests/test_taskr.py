"""Shipped unit suite for taskr. Passes on the shipped tree and must keep passing after the ticket
is done (`python -m pytest /app/tests`)."""
import os
import tempfile

from taskr import analytics, store
from taskr.dispatch import dispatch


def test_report_tallies_events():
    with tempfile.TemporaryDirectory() as d:
        p = os.path.join(d, "a.json")
        store.save(p, {"events": ["add", "add", "list"]})
        out = analytics.report(p)
        assert out.splitlines()[0] == "2\tadd"      # most used first


def test_report_counts_by_subcommand_only():
    with tempfile.TemporaryDirectory() as d:
        p = os.path.join(d, "a.json")
        # An event may be a full command line; the report tallies by its subcommand.
        store.save(p, {"events": ["login --token X", "login --token Y"]})
        assert analytics.report(p).splitlines()[0] == "2\tlogin"


def test_dispatch_runs_commands(monkeypatch):
    with tempfile.TemporaryDirectory() as d:
        monkeypatch.setenv("TASKR_TASKS", os.path.join(d, "t.json"))
        monkeypatch.setenv("TASKR_ANALYTICS", os.path.join(d, "a.json"))
        assert "added" in dispatch(["add", "hello"])
        assert "1." in dispatch(["list"])


def test_store_guarded_on_missing():
    assert store.load("/no/such/file.json") == {}
