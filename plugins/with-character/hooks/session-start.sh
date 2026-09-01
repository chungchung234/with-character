#!/bin/bash
set -e
WORKSPACE="${CLAUDE_PROJECT_DIR:-${PWD}}"
CONFIG="${WORKSPACE}/.claude/with-character.local.md"
COMPILER="${CLAUDE_PLUGIN_ROOT}/scripts/compile_character.mjs"
CONTEXT="$(node "$COMPILER" "$CONFIG")"
[ -z "$CONTEXT" ] && exit 0
node -e 'process.stdout.write(JSON.stringify({hookSpecificOutput:{hookEventName:"SessionStart",additionalContext:process.argv[1]}}))' "$CONTEXT"
