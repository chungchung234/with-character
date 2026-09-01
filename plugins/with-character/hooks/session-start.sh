#!/bin/bash
set -e
CONFIG="${CLAUDE_PROJECT_DIR:-.}/.claude/with-character.local.md"
COMPILER="${CLAUDE_PLUGIN_ROOT}/scripts/compile_character.py"
CONTEXT="$(python3 "$COMPILER" "$CONFIG")"
[ -z "$CONTEXT" ] && exit 0
python3 -c 'import json,sys; print(json.dumps({"hookSpecificOutput":{"hookEventName":"SessionStart","additionalContext":sys.argv[1]}}, ensure_ascii=False))' "$CONTEXT"
