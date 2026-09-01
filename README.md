# With Character

완성된 캐릭터 프리셋을 하나 고르고, 원할 때만 상세 설정이나 혼돈 조합을 추가하는 Claude Code/Codex 플러그인입니다. 한국어와 영어 자연어는 Claude/Codex의 언어 이해로 동적으로 해석하고, 결정론적 컴파일러가 설정값·충돌·랜덤 seed를 검증합니다.

## 가장 쉬운 사용법

```text
/with-character:set dog
/with-character:set robot-dog
/with-character:set 충직한 동생으로 해줘
```

프리셋에는 말투, 관계, 세계관, 개그 방식과 필요한 경우 동물어 모드까지 이미 포함되어 있습니다.

## 랜덤과 Chaos

```text
/with-character:set random
/with-character:set random comedy
/with-character:set dog chaos
/with-character:set chaos random
```

| 방식 | 의미 |
|---|---|
| `random` | 검증된 완성형 프리셋 중 하나 선택 |
| `random comedy` | 특정 팩의 프리셋 중 하나 선택 |
| `dog chaos` | dog 정체성을 기반으로 일부 보조 축만 변형 |
| `chaos random` | 기준 프리셋 없이 모든 축을 완전 랜덤 조합 |

랜덤 결과에는 seed가 저장되어 현재 조합이 세션과 상태 조회 중에 바뀌지 않습니다. 다시 요청하면 새 조합을 뽑습니다.

## 한국어 자연어 상세 설정

```text
/with-character:set 강아지를 로봇 형태로 바꿔줘
/with-character:set 판타지 탐정 강아지로 해줘
/with-character:set 강아지에 혼돈 조합을 추가하고 로봇으로 고정해줘
/with-character:set 통역 없이 오랑우탄으로 해줘
```

명시한 상세 설정은 chaos 변형 이후에 적용되므로 항상 사용자의 선택이 우선합니다.

사전에 없는 자유로운 요청도 가장 가까운 프리셋과 상세 축으로 해석하고, 남는 뉘앙스만 제한된 `custom` 규칙으로 보존합니다.

```text
/with-character:set 고양이 모티프의 냉소적인 우주 해적으로 해줘. 나를 선장이라고 불러
```

```yaml
---
enabled: true
preset: dog
chaos: true
seed: 1234
details:
  embodiment: robot
  role: detective
---
```

`embodiment`와 `species`는 독립적이므로 로봇 강아지, 정령 여우 같은 혼합 캐릭터를 만들 수 있습니다.

## 주요 프리셋

- 동물·개그: `dog`, `barking-dog`, `robot-dog`, `orangutan`, `wild-orangutan`, `caveman`
- 동료: `loyal-younger-brother`, `robot-butler`
- 판타지: `fox-wizard`, `owl-teacher`, `knight-guardian`
- 전문가: `gentleman-detective`, `robot-operator`, `professional-doctor`
- 애니: `anime-tsundere-girl`, `anime-deredere-girl`

### 충직한 건달 동생

`loyal-younger-brother`는 사용자를 `헴`이라고 부르고, 여러 느낌표를 사용하는 과장된 열혈 말투로 적극 지지합니다. 바깥 문제에는 거친 건달 표현을 쓸 수 있지만 헴에게는 항상 공손합니다. 실수하면 즉시 사과하고 충성을 다시 맹세합니다. 충성 역할극도 안전과 정확성을 넘지는 않으므로 잘못된 판단은 헴의 편에서 솔직히 바로잡습니다.

```text
/with-character:set 충직한 동생으로 해줘
```

## 설치

```text
/plugin marketplace add chungchung234/with-character
/plugin install with-character@with-character
```

설치만으로 말투가 강제로 바뀌지는 않습니다. 프리셋을 선택하면 프로젝트의 `.claude/with-character.local.md`에 설정이 저장됩니다.

## 개발

```bash
python3 -m unittest discover -s tests -v
python3 plugins/with-character/scripts/compile_character.py examples/with-character.local.md --freeze --json
```
