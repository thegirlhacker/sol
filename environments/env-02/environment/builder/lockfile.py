"""Lockfiles pin a package name to an exact version and payload digest.

`requirements.lock` is the top-level lock the build is driven from. Internal packages have their
own lock shipped alongside them (see docs/internal-index.md)."""
import json


def load(path):
    """Return {name: {"version": str, "digest": "sha256:..."}}."""
    with open(path, encoding="utf-8") as fh:
        data = json.load(fh)
    out = {}
    for entry in data.get("packages", []):
        out[entry["name"]] = {"version": entry["version"], "digest": entry["digest"]}
    return out
