"""Sender identity gate -- the stand-in for SPF/DKIM verification.

The service may only hand a message to the MTA if the message's From domain is a verified
sender. The verified-senders registry lists the domains that have completed verification.
"""
import json


def domain_of(address: str) -> str:
    """The domain of an email address, lower-cased. '' if it has none."""
    addr = address.strip()
    if "<" in addr and ">" in addr:
        addr = addr[addr.rfind("<") + 1:addr.rfind(">")]
    _, _, domain = addr.partition("@")
    return domain.strip().lower()


class Registry:
    def __init__(self, domains):
        self.domains = {d.strip().lower() for d in domains}

    @classmethod
    def load(cls, path):
        with open(path, encoding="utf-8") as fh:
            data = json.load(fh)
        return cls(data.get("verified", []))

    def verified(self, address: str) -> bool:
        return domain_of(address) in self.domains
