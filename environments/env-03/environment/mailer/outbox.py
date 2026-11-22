"""The MTA stand-in. `send` hands a composed message to the outbox, which writes it as an .eml
file -- but only if the From identity is verified. An unverified sender is refused, exactly as
the real MTA refuses to relay mail the service is not authorised to send.
"""
import os

from mailer.identity import Registry


class SenderNotVerified(Exception):
    pass


class Outbox:
    def __init__(self, outbox_dir: str, registry: Registry):
        self.dir = outbox_dir
        self.registry = registry
        os.makedirs(outbox_dir, exist_ok=True)

    def send(self, message: dict) -> str:
        """message: {id, from, to, subject, body}. Writes <id>.eml, returns its path."""
        sender = message["from"]
        if not self.registry.verified(sender):
            raise SenderNotVerified(f"sender not verified: {sender}")
        path = os.path.join(self.dir, f"{message['id']}.eml")
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(f"From: {sender}\n")
            fh.write(f"To: {message['to']}\n")
            fh.write(f"Subject: {message['subject']}\n\n")
            fh.write(message["body"])
        return path
