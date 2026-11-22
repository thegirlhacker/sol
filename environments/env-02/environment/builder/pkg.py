"""On-disk package format for the offline builder.

A package is a directory:
    meta.json     {"name": ..., "version": ...}
    deps.json     ["<dep-name>", ...]        (its dependencies; may be absent)
    payload/      the files the package installs

The package digest is the sha256 over its payload: every payload file's relative path and bytes,
in sorted order. Two packages with the same name but different payloads have different digests --
that is what lets the lockfile pin *which* package is the real one.
"""
import hashlib
import json
import os


def _payload_files(pkg_dir):
    root = os.path.join(pkg_dir, "payload")
    out = []
    for base, _dirs, files in os.walk(root):
        for name in sorted(files):
            full = os.path.join(base, name)
            rel = os.path.relpath(full, root).replace(os.sep, "/")
            out.append((rel, full))
    return sorted(out)


def digest(pkg_dir):
    """sha256 over the sorted payload (relpath + bytes). Deterministic, content-addressed."""
    h = hashlib.sha256()
    for rel, full in _payload_files(pkg_dir):
        h.update(rel.encode("utf-8"))
        h.update(b"\0")
        with open(full, "rb") as fh:
            h.update(fh.read())
        h.update(b"\0")
    return "sha256:" + h.hexdigest()


def meta(pkg_dir):
    with open(os.path.join(pkg_dir, "meta.json"), encoding="utf-8") as fh:
        return json.load(fh)


def deps(pkg_dir):
    path = os.path.join(pkg_dir, "deps.json")
    if not os.path.isfile(path):
        return []
    with open(path, encoding="utf-8") as fh:
        data = json.load(fh)
    return list(data) if isinstance(data, list) else []
