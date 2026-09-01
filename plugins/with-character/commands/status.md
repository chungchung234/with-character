---
description: 현재 캐릭터 조합 확인
---
Claude Code에서는 프로젝트, Cowork에서는 현재 작업공간의 `.claude/with-character.local.md`를 `node "${CLAUDE_PLUGIN_ROOT}/scripts/compile_character.mjs" "${CLAUDE_PROJECT_DIR:-${PWD}}/.claude/with-character.local.md" --json`으로 해석해 활성화 여부, 출력 언어, 선택 전략, 프리셋, 캐릭터 표시명과 chaos 변화만 먼저 보여주세요. 설정된 locale 언어로 답하고, 사용자가 상세 정보를 요청한 경우에만 최종 traits를 펼쳐 보여주세요. 파일이 없으면 사용자 요청 언어로 스타일이 꺼져 있음을 안내하세요.
