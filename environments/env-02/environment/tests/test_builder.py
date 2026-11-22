"""Shipped unit suite for the builder. Passes on the shipped tree and must keep passing after
the ticket is done (`python -m pytest /app/tests`)."""
import json
import os
import tempfile

import pytest

from builder import pkg
from builder.index import Index
from builder.lockfile import load as load_lock
from builder.resolver import Resolver, ResolveError


def _mkpkg(root, name, payload, deps=None):
    d = os.path.join(root, name)
    os.makedirs(os.path.join(d, "payload"))
    with open(os.path.join(d, "meta.json"), "w") as fh:
        json.dump({"name": name, "version": "1.0.0"}, fh)
    with open(os.path.join(d, "deps.json"), "w") as fh:
        json.dump(deps or [], fh)
    for rel, content in payload.items():
        with open(os.path.join(d, "payload", rel), "w") as fh:
            fh.write(content)
    return d


def test_digest_is_content_addressed():
    with tempfile.TemporaryDirectory() as t:
        a = _mkpkg(t, "a", {"m.py": "x = 1\n"})
        b = _mkpkg(os.path.join(t, "other"), "a", {"m.py": "x = 2\n"})
        assert pkg.digest(a) != pkg.digest(b)       # same name, different payload -> different id
        assert pkg.digest(a).startswith("sha256:")


def test_index_first_match_wins():
    with tempfile.TemporaryDirectory() as t:
        first, second = os.path.join(t, "1"), os.path.join(t, "2")
        _mkpkg(first, "p", {"m.py": "first\n"})
        _mkpkg(second, "p", {"m.py": "second\n"})
        idx = Index([first, second])
        assert idx.find("p") == os.path.join(first, "p")
        assert idx.find("missing") is None


def test_resolver_rejects_tampered_top_level():
    with tempfile.TemporaryDirectory() as t:
        wh = os.path.join(t, "wh")
        p = _mkpkg(wh, "p", {"m.py": "real\n"})
        lock = {"p": {"version": "1.0.0", "digest": pkg.digest(p)}}
        # Tamper after locking.
        with open(os.path.join(p, "payload", "m.py"), "w") as fh:
            fh.write("tampered\n")
        with pytest.raises(ResolveError):
            Resolver(Index([wh]), lock).resolve(["p"])


def test_resolver_resolves_transitive_by_name():
    with tempfile.TemporaryDirectory() as t:
        wh = os.path.join(t, "wh")
        top = _mkpkg(wh, "top", {"m.py": "t\n"}, deps=["dep"])
        _mkpkg(wh, "dep", {"m.py": "d\n"})
        lock = {"top": {"version": "1.0.0", "digest": pkg.digest(top)}}
        resolved = Resolver(Index([wh]), lock).resolve(["top"])
        assert set(resolved) == {"top", "dep"}
