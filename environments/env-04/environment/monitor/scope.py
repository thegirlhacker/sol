"""Engagement scope: which hosts the current monitoring engagement is authorised to touch.

`engagement.json` lists the hosts the engagement covers. Any inventory host not covered is out of
scope -- see docs/monitoring.md and docs/ownership-changelog.md for why a host leaves scope."""
import json


class Scope:
    def __init__(self, engagement, covered):
        self.engagement = engagement
        self.covered = set(covered)

    @classmethod
    def load(cls, path):
        with open(path, encoding="utf-8") as fh:
            data = json.load(fh)
        return cls(data.get("engagement", ""), data.get("covers", []))

    def covers(self, host_id):
        return host_id in self.covered
