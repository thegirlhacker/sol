"""`python -m builder build` -- run the offline build from build.json."""
import argparse
import sys

from builder.build import Build


def main(argv=None):
    p = argparse.ArgumentParser(prog="builder")
    sub = p.add_subparsers(dest="cmd", required=True)
    b = sub.add_parser("build", help="assemble the install tree")
    b.add_argument("--config", default="/app/build.json")
    args = p.parse_args(argv)
    if args.cmd == "build":
        names = Build.load(args.config).run()
        print("build: installed " + ", ".join(names))
        return 0
    p.error("unknown command")


if __name__ == "__main__":
    sys.exit(main())
