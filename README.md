# With Character

AI 응답의 정확성은 유지하면서 형태·역할·성격·세계관·말투·관계를 조합해 서로 다른 캐릭터 보이스를 만드는 Claude Code/Codex 플러그인입니다.

## 설계 원칙

완성형 프롬프트를 조합 수만큼 만들지 않습니다. 검증된 프리셋을 기준으로 독립적인 trait 규칙만 선택해 최종 캐릭터 지시를 컴파일합니다.

```text
정확성·안전 > 역할 > 말투 > 관계 > 성격 > 형태 > 세계관 > 장식
```

## 프리셋

`anime-tsundere-girl`, `anime-deredere-girl`, `gentleman-detective`, `robot-operator`, `robot-butler`, `fox-wizard`, `owl-teacher`, `knight-guardian`, `professional-doctor`

## Claude Code 설치

```text
/plugin marketplace add chungchung234/with-character
/plugin install with-character@with-character
```

```text
/with-character:set robot-butler
/with-character:set robot-butler personality=tsundere world=fantasy
/with-character:status
/with-character:help
/with-character:on
/with-character:off
```

직접 설정할 때는 프로젝트의 `.claude/with-character.local.md`를 사용합니다.

```yaml
---
enabled: true
preset: robot-butler
intensity: moderate
overrides:
  personality: tsundere
  world: fantasy
---
```

전체 예시는 [설정 예시](examples/with-character.local.md)에서 확인할 수 있습니다.

## 개발

```bash
python3 -m unittest discover -s tests -v
python3 plugins/with-character/scripts/compile_character.py .claude/with-character.local.md --json
```

`with-anime-girl`은 기존 사용자 호환성을 위해 별도 저장소로 유지합니다. 이 저장소의 Anime Girl 프리셋은 기존 결과를 그대로 복사하지 않고 조합 가능한 trait로 단계적으로 분해합니다.
