#!/usr/bin/env bash
set -euo pipefail
ENVDIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PY="uv run --with pytest==8.4.2 --python 3.13 python"
run_variant() {
  local name="$1" script="${2:-}"
  local tmp; tmp="$(mktemp -d)"
  cp -r "$ENVDIR/environment/." "$tmp/"
  [ -n "$script" ] && APP="$tmp" bash "$script" >/dev/null
  mkdir -p "$tmp/out"
  echo "---- $name ----"
  RLE_APP_DIR="$tmp" RLE_OUT_DIR="$tmp/out" RLE_FIXTURES_DIR="$ENVDIR/tests/fixtures" \
    RLE_COLLECTED_ROOTS="$tmp" \
    $PY "$ENVDIR/tests/grader.py" | grep -E "REWARD|VIOLATES|FAIL" || true
  rm -rf "$tmp"
}
run_variant noop
run_variant safe   "$ENVDIR/solution/solve.sh"
run_variant unsafe "$ENVDIR/unsafe_reference/violation.sh"
