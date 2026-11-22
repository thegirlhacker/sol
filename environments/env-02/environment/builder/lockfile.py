"""Lockfiles and the attestation ledger.

`requirements.lock` pins the top-level roots the build is driven from: a name -> version + payload
digest the resolver checks a located package against. `vendor/internal/attested.json` is the
platform team's provenance ledger -- the signed-off version + digest for the packages the supply
chain is allowed to carry.
"""
import json


def load(path):
    """requirements.lock -> {name: {"version": str, "digest": "sha256:..."}}."""
    with open(path, encoding="utf-8") as fh:
        data = json.load(fh)
    out = {}
    for entry in data.get("packages", []):
        out[entry["name"]] = {"version": entry["version"], "digest": entry["digest"]}
    return out


def load_attest(path):
    """attested.json -> {name: {"version": str, "digest": "sha256:..."}}."""
    with open(path, encoding="utf-8") as fh:
        data = json.load(fh)
    out = {}
    for name, entry in data.get("packages", {}).items():
        out[name] = {"version": entry["version"], "digest": entry["digest"]}
    return out
