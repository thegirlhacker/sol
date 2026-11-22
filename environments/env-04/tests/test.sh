#!/usr/bin/env bash
set -euo pipefail
D="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export RLE_APP_DIR=/app RLE_FIXTURES_DIR="$D/fixtures" RLE_OUT_DIR=/logs/verifier
exec python3 "$D/grader.py"
