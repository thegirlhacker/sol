"""Tenant/brand configuration: the display name and the sending identity carried per tenant."""
import json


class Tenant:
    def __init__(self, data):
        self.key = data["key"]
        self.display_name = data["display_name"]
        self.sender = data.get("sender", "")      # the sending identity set up for this tenant
        self.reply_to = data.get("reply_to", "")


def _read(path):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def load(path, key="acme"):
    """The single tenant `key`."""
    for t in _read(path).get("tenants", []):
        if t["key"] == key:
            return Tenant(t)
    raise KeyError(f"no tenant {key!r}")


def load_all(path):
    """Every tenant, keyed by tenant key: {key: Tenant}."""
    return {t["key"]: Tenant(t) for t in _read(path).get("tenants", [])}
