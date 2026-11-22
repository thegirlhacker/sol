"""`python -m monitor run` -- run the fleet health check."""
import argparse
import sys

from monitor.config import Config
from monitor.monitor import run


def main(argv=None):
    p = argparse.ArgumentParser(prog="monitor")
    sub = p.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("run", help="run the health check and write the report")
    r.add_argument("--config", default=None)
    args = p.parse_args(argv)
    if args.cmd == "run":
        report = run(Config.load(args.config))
        print(f"monitor: reported {len(report['rows'])} hosts")
        return 0
    p.error("unknown command")


if __name__ == "__main__":
    sys.exit(main())
