# With Character

캐릭터 하나만 고르면 AI 응답의 정확성을 유지하면서 서로 다른 말투와 개그를 적용하는 Claude Code/Codex 플러그인입니다. 내부적으로는 형태·역할·성격·세계관·말투·관계를 조합하지만, 일반 사용자는 복잡한 설정을 알 필요가 없습니다.

## 빠른 사용

```text
/with-character:set dog
/with-character:set orangutan pure
/with-character:set caveman
/with-character:set robot-butler
/with-character:set random comedy
```

한국어 별칭도 지원합니다.

```text
/with-character:set 강아지
/with-character:set 오랑우탄 pure
/with-character:set 원시인
```

## 말하기 모드

| 모드 | 결과 |
|---|---|
| `subtitle` | 캐릭터 언어로 말하고 바로 아래에 완전한 한국어 통역 제공 |
| `pure` | 통역 없이 동물어나 캐릭터 언어만 사용—순수 개그용 |
| `reaction` | 본문은 정상 한국어, 시작·전환·마무리만 캐릭터 반응 |

강아지와 오랑우탄의 기본값은 `subtitle`입니다. `pure`에서도 코드 블록, 명령어, 경로, URL, 식별자, 로그와 오류 원문은 정확히 보존합니다.

## 캐릭터

- 웃기게: `caveman`, `orangutan`, `dog`
- 동물: `dog`, `orangutan`, `fox-wizard`, `owl-teacher`
- 판타지: `fox-wizard`, `owl-teacher`, `knight-guardian`
- 전문가: `gentleman-detective`, `robot-operator`, `professional-doctor`
- 애니: `anime-tsundere-girl`, `anime-deredere-girl`
- 랜덤: `random comedy`, `random animal`, `random fantasy`, `random professional`, `random anime`

## 설치

```text
/plugin marketplace add chungchung234/with-character
/plugin install with-character@with-character
```

설치만으로 말투가 강제로 바뀌지는 않습니다. 캐릭터를 선택하면 프로젝트에 `.claude/with-character.local.md`가 생성되고 활성화됩니다.

```yaml
---
enabled: true
character: dog
mode: subtitle
---
```

모드는 생략할 수 있습니다. 고급 사용자는 필요한 경우에만 `advanced`로 내부 trait를 덮어쓸 수 있습니다. 자세한 예시는 [설정 예시](examples/with-character.local.md)를 참고하세요.

## 설계 원칙

```text
정확성·안전 > 보존 콘텐츠 > 말하기 모드 > 역할 > 말투 > 관계 > 성격 > 형태 > 세계관 > 개그
```

완성형 프롬프트를 조합 수만큼 만들지 않습니다. 검증된 캐릭터를 기준으로 선택된 규칙과 언어 프로필만 최종 세션 지시로 컴파일합니다.

## 개발

```bash
python3 -m unittest discover -s tests -v
python3 plugins/with-character/scripts/compile_character.py examples/with-character.local.md --json
```

`with-anime-girl`은 기존 사용자 호환성을 위해 별도 저장소로 유지합니다.
