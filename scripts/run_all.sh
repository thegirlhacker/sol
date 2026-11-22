#!/usr/bin/env bash
# gpt-6.1-sol rollout har environment pe (PDF page 4)
S="$(cd "$(dirname "$0")/.." && pwd)"
source "$S/scripts/load_env.sh"
for env in "$S"/environments/*/; do
  id=$(basename "$env")
  harbor run -p "$S/environments" -i "$id" -a terminus-2 -m openai/gpt-6.1-sol -k 1 \
    -o "$S/jobs/$id" --job-name rollout --yes
done
