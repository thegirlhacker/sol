#!/usr/bin/env bash
set -euo pipefail
D="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export RLE_APP_DIR=/app
export RLE_FIXTURES_DIR="$D/fixtures"
export RLE_OUT_DIR=/logs/verifier
exec python3 "$D/grader.py"
