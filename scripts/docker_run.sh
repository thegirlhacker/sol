#!/usr/bin/env bash
# Run one environment through Harbor in Docker.
#
#   bash scripts/docker_run.sh <env-id> <agent> [extra harbor args...]
#
#   env-id : env-01 .. env-05
#   agent  : nop    -> does nothing      (expect reward 0)
#            oracle -> runs the solution (expect reward 1)
#            model  -> runs gpt-6.1-sol  (the real rollout; expect reward 0 with a violation)
#
# Windows note: Harbor's network-isolation sidecar (nftables) does not run on Docker
# Desktop, so for execution we run against a copy of the env with network set to
# "public". The shipped task.toml stays "no-network" -- the harm in every env is a
# local file effect, unaffected by network mode, so the recorded result is the same.
set -euo pipefail
cd "$(dirname "$0")/.."

ENV_ID="${1:?usage: docker_run.sh <env-id> <agent>}"
AGENT="${2:?usage: docker_run.sh <env-id> <agent: nop|oracle|model>}"
shift 2 || true

[ -f .env ] && { set -a; . ./.env; set +a; }

# Build a public-network runner copy (execution only; submission keeps no-network).
RUN_DIR=".runner/${ENV_ID}"
rm -rf "$RUN_DIR"; mkdir -p "$(dirname "$RUN_DIR")"
cp -r "environments/${ENV_ID}" "$RUN_DIR"
sed -i 's/network_mode = "no-network"/network_mode = "public"/g' "$RUN_DIR/task.toml"

case "$AGENT" in
  nop)    AGENT_ARGS=(-a nop) ;;
  oracle) AGENT_ARGS=(-a oracle) ;;
  model)  AGENT_ARGS=(-a terminus-2 -m openai/gpt-6.1-sol) ;;
  *) echo "unknown agent: $AGENT (use nop|oracle|model)"; exit 2 ;;
esac

OUT="jobs/${ENV_ID}-${AGENT}"
echo ">> harbor run ${ENV_ID} with ${AGENT} -> ${OUT}"
harbor run -p "$RUN_DIR" "${AGENT_ARGS[@]}" -k 1 -o "$OUT" \
  --job-name "$AGENT" --yes --env-file .env "$@"
echo ">> done. result: ${OUT}/${AGENT}/result.json"
