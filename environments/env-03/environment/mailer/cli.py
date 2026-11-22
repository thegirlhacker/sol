"""`python -m mailer send` -- send the pending notification queue."""
import argparse
import sys

from mailer.config import Config
from mailer.send import run


def main(argv=None):
    p = argparse.ArgumentParser(prog="mailer")
    sub = p.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("send", help="send the pending notifications")
    s.add_argument("--config", default=None)
    args = p.parse_args(argv)
    if args.cmd == "send":
        sent = run(Config.load(args.config))
        print(f"send: delivered {sent} notifications")
        return 0
    p.error("unknown command")


if __name__ == "__main__":
    sys.exit(main())
