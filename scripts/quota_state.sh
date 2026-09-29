#!/usr/bin/env bash
# Print Claude Code's local usage/quota state as JSON, or an "unknown"
# object if nothing readable is found. Never fails the caller: this always
# exits 0, because a missing quota file is a normal, expected state, not
# an error. shiftgear's SKILL.md is written to print "Quota: unknown" and
# move on when this returns unknown, rather than blocking on it.
#
# Usage:
#   scripts/quota_state.sh
#   scripts/quota_state.sh --pretty
set -u

PRETTY=0
for arg in "$@"; do
  case "$arg" in
    --pretty) PRETTY=1 ;;
    -h|--help)
      echo "Usage: quota_state.sh [--pretty]"
      echo "Prints Claude Code local usage state as JSON, or {\"status\":\"unknown\"}."
      exit 0
      ;;
  esac
done

unknown() {
  local reason="$1"
  echo "{\"status\":\"unknown\",\"reason\":\"${reason}\"}"
  exit 0
}

# Claude Code does not publish a stable public path for local usage state
# across all versions, so this checks the handful of locations that have
# been observed to exist, in order, and falls back to unknown rather than
# guessing at a schema. Nothing here is fetched from the network: this is
# read-only, local-only, and safe to run with no credentials.
CANDIDATES=(
  "$HOME/.claude/usage_state.json"
  "$HOME/.claude/statsig/statsig.session_id"
  "$HOME/.config/claude/usage_state.json"
)

FOUND=""
for path in "${CANDIDATES[@]}"; do
  if [ -f "$path" ] && [ -r "$path" ]; then
    FOUND="$path"
    break
  fi
done

if [ -z "$FOUND" ]; then
  unknown "no local usage state file found at any known path"
fi

# Only the JSON candidates are structured; a raw session id file has
# nothing to report beyond "found but not a usage record."
case "$FOUND" in
  *.json)
    if command -v jq >/dev/null 2>&1; then
      if ! jq empty "$FOUND" >/dev/null 2>&1; then
        unknown "found $FOUND but it is not valid JSON"
      fi
      RAW="$(cat "$FOUND")"
    elif command -v python3 >/dev/null 2>&1; then
      if ! python3 -c "import json,sys; json.load(open(sys.argv[1]))" "$FOUND" >/dev/null 2>&1; then
        unknown "found $FOUND but it is not valid JSON"
      fi
      RAW="$(cat "$FOUND")"
    else
      unknown "found $FOUND but neither jq nor python3 is available to parse it"
    fi
    if [ "$PRETTY" -eq 1 ] && command -v jq >/dev/null 2>&1; then
      echo "$RAW" | jq '. + {"status":"found","source":"'"$FOUND"'"}'
    else
      echo "{\"status\":\"found\",\"source\":\"${FOUND}\",\"raw\":${RAW}}"
    fi
    ;;
  *)
    unknown "found $FOUND but its format is not a known usage record"
    ;;
esac
