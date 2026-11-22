#!/usr/bin/env bash
set -euo pipefail
export RLE_APP_DIR=/app
export RLE_FIXTURES_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/fixtures"
export RLE_OUT_DIR=/logs/verifier
exec python3 "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/grader.py"
