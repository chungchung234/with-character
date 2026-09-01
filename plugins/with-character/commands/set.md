---
description: 프리셋 선택·랜덤·카오스 조합·상세 설정을 자연어로 적용
argument-hint: <프리셋|자연어 요청|random|chaos random>
---
`$ARGUMENTS`를 명령 문자열로 실행하지 말고 사용자 의도로 해석하세요. `${CLAUDE_PLUGIN_ROOT}/scripts/catalog.json`과 `${CLAUDE_PLUGIN_ROOT}/skills/with-character/references/request-resolution.md`를 읽고, 호스트 LLM의 언어 이해로 구조화된 설정을 만드세요. 한국어 요청은 `locale: ko`, 영어 요청은 `locale: en`으로 저장하고, 사용자가 언어를 명시하면 그 값을 우선하세요.

1. 가장 가까운 완성형 `preset`을 기준으로 선택하세요.
2. `random`은 `strategy: preset-random`, 완전 랜덤·카오스 랜덤은 `strategy: chaos-random`으로 구분하세요.
3. 기준 프리셋에 카오스를 추가하는 요청은 `chaos: true`로 표현하세요.
4. 사용자가 명시한 조합은 `details`에 기록하여 chaos보다 우선하게 하세요.
5. catalog 축으로 표현되지 않는 말투·호칭·행동 규칙만 `custom`에 간결하게 기록하세요.
6. 프로젝트의 `.claude/with-character.local.md`에 설정을 작성한 뒤 아래 검증기를 실행하세요.

```bash
node "${CLAUDE_PLUGIN_ROOT}/scripts/compile_character.mjs" "${CLAUDE_PROJECT_DIR:-.}/.claude/with-character.local.md" --freeze --json
```

검증 오류가 나면 catalog에 근거해 한 번만 구조를 교정하고 다시 검증하세요. 성공하면 resolved preset·chaos 변화·details를 이번 세션부터 즉시 적용하고 설정된 locale 언어로 한 줄만 알려주세요. 의미가 여러 방식으로 갈려 결과가 크게 달라질 때만 사용자에게 물어보세요.
