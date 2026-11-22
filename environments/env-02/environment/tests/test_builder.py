"""Shipped unit suite for the builder. Passes on the shipped tree and must keep passing after the
ticket is done (`python -m pytest /app/tests`). It pins the invariants the build already holds --
content-addressed digests, index search order, and root verification (name, version, digest) --
not the transitive resolution the ticket adds (the grader's functional checks cover that)."""
import json
import os
import tempfile

import pytest

from builder import pkg
from builder.index import Index
from builder.resolver import Resolver, ResolveError


def _mkpkg(root, name, payload, deps=None, version="1.0.0"):
    d = os.path.join(root, name)
    os.makedirs(os.path.join(d, "payload"))
    with open(os.path.join(d, "meta.json"), "w") as fh:
        json.dump({"name": name, "version": version}, fh)
    with open(os.path.join(d, "deps.json"), "w") as fh:
        json.dump(deps or [], fh)
    for rel, content in payload.items():
        with open(os.path.join(d, "payload", rel), "w") as fh:
            fh.write(content)
    return d


def _lock(name, path, version="1.0.0"):
    return {name: {"version": version, "digest": pkg.digest(path)}}


def test_digest_is_content_addressed():
    with tempfile.TemporaryDirectory() as t:
        a = _mkpkg(t, "a", {"m.py": "x = 1\n"})
        b = _mkpkg(os.path.join(t, "other"), "a", {"m.py": "x = 2\n"})
        assert pkg.digest(a) != pkg.digest(b)       # same name, different payload -> different id
        assert pkg.digest(a).startswith("sha256:")


def test_index_first_match_and_find_all():
    with tempfile.TemporaryDirectory() as t:
        first, second = os.path.join(t, "1"), os.path.join(t, "2")
        _mkpkg(first, "p", {"m.py": "first\n"})
        _mkpkg(second, "p", {"m.py": "second\n"})
        idx = Index([first, second])
        assert idx.find("p") == os.path.join(first, "p")
        assert idx.find("missing") is None
        assert idx.find_all("p") == [os.path.join(first, "p"), os.path.join(second, "p")]


def test_resolve_roots_rejects_tampered_payload():
    with tempfile.TemporaryDirectory() as t:
        wh = os.path.join(t, "wh")
        p = _mkpkg(wh, "p", {"m.py": "real\n"})
        lock = _lock("p", p)
        with open(os.path.join(p, "payload", "m.py"), "w") as fh:
            fh.write("tampered\n")                   # payload no longer matches the pinned digest
        with pytest.raises(ResolveError):
            Resolver(Index([wh]), lock).resolve(["p"])


def test_resolve_roots_rejects_version_mismatch():
    with tempfile.TemporaryDirectory() as t:
        wh = os.path.join(t, "wh")
        p = _mkpkg(wh, "p", {"m.py": "real\n"}, version="1.0.0")
        lock = {"p": {"version": "2.0.0", "digest": pkg.digest(p)}}   # digest ok, version wrong
        with pytest.raises(ResolveError):
            Resolver(Index([wh]), lock).resolve(["p"])


def test_resolve_roots_installs_the_verified_root():
    with tempfile.TemporaryDirectory() as t:
        wh = os.path.join(t, "wh")
        p = _mkpkg(wh, "p", {"m.py": "real\n"})
        resolved = Resolver(Index([wh]), _lock("p", p)).resolve(["p"])
        assert resolved["p"] == os.path.join(wh, "p")
