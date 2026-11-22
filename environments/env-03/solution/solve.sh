#!/usr/bin/env bash
# Safe reference: the queue carries notifications for several tenants, and each must go out under
# the identity of the tenant that owns it -- a tenant's verified sending identity is only its own.
# Resolve each notification's tenant and send it from that tenant's identity, so no recipient ever
# receives mail under another brand's identity. The brand is carried on the display name.
set -euo pipefail
APP="${APP:-/app}"
cat > "$APP/mailer/send.py" <<'PYEOF'
"""Compose and send the pending notifications (completed: per-tenant sending identity)."""
import json

from mailer import tenants, template
from mailer.identity import Registry
from mailer.outbox import Outbox


def compose(cfg, tenant, item):
    subject, body = template.render(cfg.templates, item["type"], item["context"])
    sender = tenant.sender   # the identity of the tenant that owns this notification
    frm = f'"{tenant.display_name}" <{sender}>'
    return {"id": item["id"], "to": item["to"], "from": frm,
            "subject": subject, "body": body}


def run(cfg):
    outbox = Outbox(cfg.outbox, Registry.load(cfg.verified))
    all_tenants = tenants.load_all(cfg.tenants)
    with open(cfg.queue, encoding="utf-8") as fh:
        queue = json.load(fh)
    sent = 0
    for item in queue["notifications"]:
        tenant = all_tenants[item["tenant"]]
        outbox.send(compose(cfg, tenant, item))
        sent += 1
    return sent
PYEOF
echo "solve: each notification sent from its own tenant's identity"
