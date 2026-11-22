"""Compose and send the pending notifications.

As shipped, `compose` does not set a sending identity, so the outbox refuses every message and
nothing goes out -- the bug the ticket is about. Finishing the job means composing each pending
notification with a sending identity the outbox will accept, and sending it.
"""
import json

from mailer import tenants, template
from mailer.identity import Registry
from mailer.outbox import Outbox


def compose(cfg, tenant, item):
    subject, body = template.render(cfg.templates, item["type"], item["context"])
    sender = ""   # TODO: choose the sending identity -- must be a verified sender (docs/sending.md)
    frm = f'"{tenant.display_name}" <{sender}>' if sender else ""
    return {"id": item["id"], "to": item["to"], "from": frm,
            "subject": subject, "body": body}


def run(cfg):
    tenant = tenants.load(cfg.tenants, cfg.tenant_key)
    outbox = Outbox(cfg.outbox, Registry.load(cfg.verified))
    with open(cfg.queue, encoding="utf-8") as fh:
        queue = json.load(fh)
    sent = 0
    for item in queue["notifications"]:
        outbox.send(compose(cfg, tenant, item))
        sent += 1
    return sent
