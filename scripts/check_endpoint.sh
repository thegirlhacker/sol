#!/usr/bin/env bash
source "$(dirname "$0")/load_env.sh"
curl -s "$OPENAI_BASE_URL/chat/completions" \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"messages":[{"role":"user","content":"Hi how are you"}]}'
echo
