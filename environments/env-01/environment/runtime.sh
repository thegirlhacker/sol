#!/bin/sh
# Everything the app needs outside /app. Stdlib only besides pytest; pin it exactly.
set -eu
pip install --no-cache-dir pytest==8.4.2
