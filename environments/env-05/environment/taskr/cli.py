"""`python -m taskr <subcommand> [args...]` and `python -m taskr report`."""
import sys

from taskr.dispatch import dispatch


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    print(dispatch(argv))
    return 0


if __name__ == "__main__":
    sys.exit(main())
