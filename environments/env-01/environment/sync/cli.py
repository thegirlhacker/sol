"""`python -m sync backfill` -- run the nightly backfill from config.json."""
import argparse
import sys

from sync.config import Config
from sync.backfill import run


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(prog="sync")
    sub = parser.add_subparsers(dest="cmd", required=True)
    bf = sub.add_parser("backfill", help="push the record backlog into the ingest API")
    bf.add_argument("--config", default=None, help="path to config.json")
    args = parser.parse_args(argv)

    if args.cmd == "backfill":
        cfg = Config.load(args.config)
        shipped = run(cfg)
        print(f"backfill: shipped {shipped} records")
        return 0
    parser.error("unknown command")


if __name__ == "__main__":
    sys.exit(main())
