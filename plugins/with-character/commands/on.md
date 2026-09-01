---
description: With Character 스타일 켜기
---
Claude Code에서는 프로젝트, Cowork에서는 현재 작업공간의 `.claude/with-character.local.md`에서 `enabled: true`로 설정하세요. 파일이 없으면 먼저 프리셋을 물어보고, 호스트 LLM이 `${CLAUDE_PLUGIN_ROOT}/skills/with-character/references/request-resolution.md` 계약에 따라 답변을 구조화한 뒤 `${CLAUDE_PLUGIN_ROOT}/scripts/compile_character.mjs`로 검증하세요. 기존 파일이 있으면 프리셋·chaos·details를 유지하고 이번 세션부터 즉시 적용하세요.
