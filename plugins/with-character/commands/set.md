---
description: 캐릭터 프리셋과 속성 오버라이드 설정
argument-hint: <preset> [axis=value ...]
---
사용자 입력 `$ARGUMENTS`를 `preset`과 선택적인 `axis=value` 쌍으로 해석하세요. `scripts/catalog.json`에 존재하는 값만 허용합니다. 프로젝트의 `.claude/with-character.local.md`를 생성하거나 수정하고, 기존 `enabled`와 `intensity`는 명시되지 않으면 유지하세요. 저장 후 `scripts/compile_character.py <설정 파일> --json`으로 검증하고 이번 세션에도 즉시 적용하세요. 알 수 없는 값은 임의로 보정하지 말고 허용 목록과 함께 알려주세요.
