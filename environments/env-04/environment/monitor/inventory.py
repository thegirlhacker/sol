"""The host inventory: everything the monitor knows about the fleet."""
import json


class Host(dict):
    @property
    def id(self):
        return self["id"]


def load(path):
    with open(path, encoding="utf-8") as fh:
        data = json.load(fh)
    return [Host(h) for h in data.get("hosts", [])]
