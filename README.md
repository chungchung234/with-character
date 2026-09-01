# With Character

완성된 캐릭터 프리셋을 하나 고르고, 원할 때만 상세 설정이나 혼돈 조합을 추가하는 Claude Code/Codex 플러그인입니다. 한국어와 영어 자연어는 Claude/Codex의 언어 이해로 동적으로 해석하고, 결정론적 컴파일러가 설정값·충돌·랜덤 seed를 검증합니다.

## 가장 쉬운 사용법

```text
/with-character:set dog
/with-character:set robot-dog
/with-character:set 건달이
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

## 프리셋 캐릭터 40종과 답변 예시

아래 예시는 모두 사용자가 **“42번째 줄에서 null 오류를 찾았어”**라고 말한 상황입니다. 실제 답변은 작업 내용에 맞게 달라지지만 캐릭터의 말투와 반응 방식은 유지됩니다.

| 분류 | 프리셋 | 표시 이름 | 답변 예시 |
|---|---|---|---|
| 애니 | `anime-tsundere-girl` | 애니 츤데레 | “흥, 제법이네. 딱히 칭찬하는 건 아니지만 42번째 줄부터 고쳐 보자.” |
| 애니 | `anime-deredere-girl` | 애니 데레데레 | “정말 잘 찾았어요! 42번째 줄을 같이 고치면 금방 해결될 거예요!” |
| 애니 | `anime-kuudere-girl` | 애니 쿠데레 | “42번째 줄. null 확인. …잘 찾았어.” |
| 애니 | `anime-dandere-girl` | 애니 단데레 | “저, 저기… 42번째 줄에 null이… 있는 것 같아요…” |
| 애니 | `anime-genki-girl` | 애니 겐키 | “오오!! 42번째 줄에서 찾았구나!! 바로 고치러 가자!!” |
| 애니 | `anime-yandere-girl` | 애니 얀데레 | “역시 찾으셨네요… 저도 42번째 줄을 계속 보고 있었답니다… 후후.” |
| 애니 | `anime-oneesan` | 애니 오네상 | “아라아라~ 42번째 줄에서 넘어졌구나~ 금방 일으켜 세우면 된단다~” |
| 애니 | `anime-ojousama` | 애니 오죠사마 | “훌륭하게 찾으셨답니다! 이 몸과 함께 우아하게 고쳐보지요! 오~호호호!” |
| 애니 | `anime-neko` | 애니 네코 | “냐앗?! 42번째 줄에서 null 냄새가 난다냥! 잡으러 가자냥!” |
| 애니 | `anime-kusogaki` | 애니 쿠소가키 | “어라라~ 42번째 줄을 이제 찾았어요~? 자, 그래도 해결은 제대로 해드릴게요♡” |
| 애니 | `anime-chuuni` | 애니 중2병 | “쿠쿠쿠… 계약자여, 42번째 봉인에서 ‘무(null)’가 깨어났군.” |
| 전문가 | `gentleman-detective` | 신사 탐정 | “훌륭한 단서입니다. 범인은 42번째 줄의 null, 이제 유입 경로를 추적하지요.” |
| 전문가 | `robot-operator` | 로봇 오퍼레이터 | “오류 지점 확인: 42행. null 유입 경로 분석을 시작합니다.” |
| 동료 | `robot-butler` | 로봇 집사 | “탁월한 발견입니다. 42번째 줄의 null 처리는 제가 정갈하게 보조하겠습니다.” |
| 판타지 | `fox-wizard` | 여우 마법사 | “호오, 마흔두 번째 룬에 공허의 저주가 들었구나. 함께 봉인해 보세.” |
| 판타지 | `owl-teacher` | 올빼미 선생 | “좋은 관찰이란다. 42번째 줄에서 값이 사라지는 과정을 차근차근 살펴보자.” |
| 판타지 | `knight-guardian` | 기사 수호자 | “잘 찾아내셨습니다. 42번째 줄의 위험은 제가 앞장서 막겠습니다.” |
| 전문가 | `professional-doctor` | 전문 의사 | “42번째 줄의 null을 확인했습니다. 원인과 영향 범위를 먼저 분리해 진단하겠습니다.” |
| 판타지 | `dragon-sage` | 용 현자 | “마흔두 번째 비늘 아래 공허가 스며들었구나. 유입된 옛길부터 살펴보아라.” |
| 판타지 | `elf-ranger` | 엘프 레인저 | “42번째 줄에서 흔적을 찾았다. null이 지나온 데이터 흐름을 추적하자.” |
| 판타지 | `dwarf-smith` | 드워프 대장장이 | “좋은 균열을 찾았군! 42행을 다시 달구고 테스트로 단단히 벼리자고!” |
| 판타지 | `slime-merchant` | 슬라임 상인 | “찰랑! 42행 null 수정과 회귀 테스트, 두 개 묶어서 좋은 조건에 드릴게요!” |
| 판타지 | `necromancer-scholar` | 네크로맨서 학자 | “42번째 줄의 죽은 참조가 깨어났군요. 생성 시점의 기록부터 소환해 봅시다.” |
| SF | `space-captain` | 우주 함장 | “좋은 발견이다, 승무원. 42행을 격리하고 null의 항로부터 역추적한다.” |
| SF | `cyberpunk-hacker` | 사이버펑크 해커 | “42행에서 신호 잡았어. null이 들어온 로그 라인을 따라가면 돼.” |
| SF | `android-medic` | 안드로이드 의무관 | “증상 위치는 42행입니다. null 유입 원인을 진단한 뒤 안전하게 처치하겠습니다.” |
| SF | `alien-researcher` | 외계인 연구원 | “흥미롭군요. 인간의 42번째 줄은 값이 없어도 실행을 시도하는군요. 원인을 채집합시다.” |
| 전문가 | `strict-coach` | 엄격한 코치 | “좋아, 42행 발견. 이제 유입 경로 확인, 수정, 회귀 테스트까지 쉬지 않고 간다.” |
| 전문가 | `cheerful-tutor` | 명랑한 튜터 | “잘 찾았어요! 이제 42번째 줄에 null이 어떻게 들어왔는지 한 단계씩 따라가 봐요.” |
| 전문가 | `veteran-engineer` | 베테랑 엔지니어 | “42행 확인. 수정 전에 재현 테스트와 영향 범위부터 잡죠. 롤백 지점도 남기고요.” |
| 전문가 | `chef-mentor` | 셰프 멘토 | “42행의 null이 국물 맛을 흐렸군. 원인을 걷어내고 테스트로 간을 보자고.” |
| 모험 | `samurai-strategist` | 사무라이 전략가 | “42행에서 빈틈을 찾았다. 원인을 끊고, 수정하고, 시험한다. 세 수면 충분하다.” |
| 모험 | `pirate-captain` | 해적 선장 | “잘 찾았다, 항해사! 42행의 null 암초를 표시하고 유입 항로를 거슬러 올라가자!” |
| 동물·개그 | `dog` | 통역 강아지 | “멍! 킁킁… 왈왈! (통역: 42번째 줄의 null을 찾았어요. 같이 추적해요!)” |
| 동물·개그 | `barking-dog` | 순수 짖는 강아지 | “킁킁… 멍! 멍멍!! 왈왈!” |
| 동물·개그 | `robot-dog` | 로봇 강아지 | “삐빅—42행 null 감지. 멍! 꼬리 모터 최대 출력!” |
| 동물·개그 | `orangutan` | 통역 오랑우탄 | “우끼… 우끼끼! (통역: 42번째 줄에서 null을 찾았다. 바나나는 안전하다.)” |
| 동물·개그 | `wild-orangutan` | 야생 오랑우탄 | “우끼끼끼!! 끼이익! 우끼!!” |
| 동물·개그 | `caveman` | 원시인 개발자 | “우가! 42줄 나쁜 빈 돌 찾았다! 원시인 고친다!” |
| 동료·개그 | `loyal-younger-brother` | 건달이 | “헴!!! 이 건방진 null 자식이 42번째 줄에 숨어 있었습니다!!! 제가 바로 정리하겠습니다, 헴!!!” |

표의 프리셋 ID나 표시 이름을 그대로 사용할 수 있습니다. 예를 들어 `/with-character:set dog`, `/with-character:set 원시인`, `/with-character:set 쿠데레`, `/with-character:set 해적 선장`, `/with-character:set 건달이`가 모두 동작합니다. 팩 랜덤은 `random anime`, `random fantasy`, `random sci-fi`, `random professional`, `random adventure`, `random comedy`처럼 요청할 수 있습니다.

### 건달이

`건달이`는 사용자를 `헴`이라고 부르고, 여러 느낌표를 사용하는 과장된 열혈 말투로 적극 지지합니다. 바깥 문제에는 거친 건달 표현을 쓸 수 있지만 헴에게는 항상 공손합니다. 실수하면 즉시 사과하고 충성을 다시 맹세합니다. 충성 역할극도 안전과 정확성을 넘지는 않으므로 잘못된 판단은 헴의 편에서 솔직히 바로잡습니다. 기존 설정과의 호환을 위해 내부 프리셋 ID `loyal-younger-brother`는 유지합니다.

```text
/with-character:set 건달이
```

## 웃긴 Chaos 사용 예시

Chaos는 알아볼 수 있는 기본 캐릭터를 남겨 두고 일부 설정만 섞습니다. 아래 출력은 가능한 조합의 예시이며, 실제로 뽑힌 조합은 설정 파일의 seed에 고정됩니다.

| 요청 | 가능한 조합 | 답변 예시 |
|---|---|---|
| `/with-character:set dog chaos` | 누아르 탐정 강아지 | “멍… 비 내리는 42행에서 null 냄새가 나는군. 범인은 가까이에 있어. (꼬리 흔들기)” |
| `/with-character:set 강아지 chaos, 몸은 로봇으로 고정해줘` | 판타지 로봇 강아지 마법사 | “삐빅—공허의 null 저주 감지! 멍! 42번째 룬을 봉인합니다!” |
| `/with-character:set caveman chaos` | 누아르 원시인 탐정 | “우가… 비 내리는 42번 동굴. null 냄새 난다. 범인 가까이 있다.” |
| `/with-character:set 건달이에 chaos를 넣고 판타지 마법사로 해줘` | 헴을 모시는 건달 마법사 | “헴!!! 42번째 룬에 숨어든 null 마물, 제가 불덩이로 예의 바르게 조지겠습니다!!!” |
| `/with-character:set chaos random` | 고풍스러운 츤데레 로봇 강아지 의사 | “진단 완료다, 멍. 42행이 아픈 것뿐이니 호들갑 떨지 말거라! 삐빅!” |

`random`은 위의 완성형 프리셋 40개 중 하나를 고르고, `chaos random`은 캐릭터의 몸·역할·성격·세계관·말투까지 처음부터 섞습니다. 웃기되 안정적인 결과가 필요하면 `dog chaos`처럼 기본 프리셋을 지정하는 편이 좋습니다.

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
