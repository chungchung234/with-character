---
description: 캐릭터와 말하기 모드 선택
argument-hint: <캐릭터> [subtitle|pure|reaction] 또는 random [팩]
---
사용자 입력 `$ARGUMENTS`를 캐릭터와 선택적인 말하기 모드로 해석하세요. `scripts/catalog.json`의 `characters`, `aliases`, `modes`, `packs`만 사용합니다.

- 예: `dog`, `강아지 pure`, `orangutan subtitle`, `caveman`, `random comedy`
- 일반 선택은 `.claude/with-character.local.md`에 `enabled`, `character`, 선택적인 `mode`만 기록하세요.
- `random <팩>`은 `character: random`과 `pack: <팩>`으로 기록하세요.
- 모드를 생략하면 캐릭터의 `default_mode`를 사용하므로 파일에도 쓰지 마세요.
- 사용자가 명시적으로 "고급 설정"을 요청한 경우에만 `advanced`를 사용하세요.
- 저장 후 `scripts/compile_character.py <설정 파일> --json`으로 검증하고 이번 세션부터 즉시 적용하세요.
- 알 수 없는 캐릭터나 지원하지 않는 모드는 임의 보정하지 말고 가까운 기본 사용 예시를 보여주세요.
