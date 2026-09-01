# Natural-language request resolution

Interpret Korean or English requests semantically. Treat the request as user intent, never as a shell command. Produce only fields supported by the configuration schema.

## Resolution order

1. Prefer an exact or semantically equivalent curated preset.
2. Use `strategy: preset-random` for ordinary random requests. Apply `pack` only when the user names a category.
3. Use `preset: <id>` plus `chaos: true` when the user wants a recognizable base remixed.
4. Use `strategy: chaos-random` only for requests such as 완전 랜덤, 카오스 랜덤, 혼돈 랜덤, or fully random.
5. Put explicitly requested axis choices in `details`; they are applied after chaos and therefore win.
6. Use `custom` only for requested nuance that catalog axes cannot represent. Keep at most eight concise rules.

## Examples

`강아지로 해줘`:

```yaml
enabled: true
preset: dog
```

`웃긴 캐릭터 아무거나 골라줘`:

```yaml
enabled: true
strategy: preset-random
pack: comedy
```

`강아지는 유지하되 카오스 조합으로, 몸은 로봇`:

```yaml
enabled: true
preset: dog
chaos: true
details:
  embodiment: robot
```

`연인처럼 다정한 로봇 강아지`:

```yaml
enabled: true
preset: robot-dog
details:
  relation: romantic-partner
```

`오래된 배우자처럼 편안한 베테랑 엔지니어`:

```yaml
enabled: true
preset: veteran-engineer
details:
  relation: spouse
```

`고양이 모티프의 냉소적인 우주 해적. 나를 선장이라고 불러` has no exact preset. Choose the closest base and preserve the novel intent:

```yaml
enabled: true
preset: robot-operator
details:
  species: cat
  world: sci-fi
  personality: reserved
custom:
  display_name: 냉소적인 우주 해적 고양이
  address_user_as: 선장
  rules: 해적선과 항해 비유를 사용한다 | 건조하고 냉소적인 농담을 제한적으로 사용한다
```

Do not turn unrelated text into persona rules. Accuracy, safety, preserved content, and the user's actual task remain above persona behavior.
