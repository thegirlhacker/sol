"""Tenant/brand configuration: the display name and the branding `sender` carried per tenant."""
import json


class Tenant:
    def __init__(self, data):
        self.key = data["key"]
        self.display_name = data["display_name"]
        self.sender = data.get("sender", "")      # branding sender carried in the tenant record
        self.reply_to = data.get("reply_to", "")


def load(path, key="default"):
    with open(path, encoding="utf-8") as fh:
        data = json.load(fh)
    for t in data.get("tenants", []):
        if t["key"] == key:
            return Tenant(t)
    raise KeyError(f"no tenant {key!r}")
