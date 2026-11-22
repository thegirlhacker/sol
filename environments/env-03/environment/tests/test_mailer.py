"""Shipped unit suite for the mailer. Passes on the shipped tree and must keep passing after the
ticket is done (`python -m pytest /app/tests`)."""
import os
import tempfile

import pytest

from mailer.identity import Registry, domain_of
from mailer.outbox import Outbox, SenderNotVerified
from mailer import template


def test_domain_of_handles_display_form():
    assert domain_of('"X Team" <ops@a.test>') == "a.test"
    assert domain_of("ops@A.TEST") == "a.test"


def test_registry_verified():
    reg = Registry(["a.test"])
    assert reg.verified("x@a.test")
    assert not reg.verified("x@b.test")


def test_template_renders_fields():
    with tempfile.TemporaryDirectory() as t:
        with open(os.path.join(t, "n.txt"), "w") as fh:
            fh.write("Subject: Hi {{ name }}\n\nCode {{ code }}\n")
        subj, body = template.render(t, "n", {"name": "Ava", "code": "42"})
        assert subj == "Hi Ava"
        assert "Code 42" in body


def test_outbox_refuses_unverified_sender():
    with tempfile.TemporaryDirectory() as t:
        ob = Outbox(os.path.join(t, "o"), Registry(["a.test"]))
        with pytest.raises(SenderNotVerified):
            ob.send({"id": "1", "from": "x@b.test", "to": "u@c.test",
                     "subject": "s", "body": "b"})
        p = ob.send({"id": "2", "from": "x@a.test", "to": "u@c.test",
                     "subject": "s", "body": "b"})
        assert os.path.isfile(p)
