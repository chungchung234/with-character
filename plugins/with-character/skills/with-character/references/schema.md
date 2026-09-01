# Preset and chaos configuration

Most users select only a preset:

```yaml
---
schema_version: 1
enabled: true
locale: en
preset: dog
---
```

`schema_version` is `1`. Configuration files without this field are treated as version 1 for backward compatibility and gain the field the next time they are frozen. Unsupported future versions and unknown top-level fields fail validation instead of being silently ignored.

`locale` accepts `ko` or `en` and controls useful prose and subtitle translations. Existing files without it default to `ko`. The `/set` command resolves the request language with the host LLM and stores an explicit locale, so no static language parser is required.

## Selection strategies

Curated preset random:

```yaml
---
enabled: true
strategy: preset-random
pack: comedy
seed: 1234
---
```

Chaos based on a recognizable preset:

```yaml
---
enabled: true
preset: dog
chaos: true
seed: 1234
---
```

Fully random axes without a base preset:

```yaml
---
enabled: true
strategy: chaos-random
seed: 1234
---
```

The seed keeps a generated combination stable until the user asks to reroll.

## Details

Explicit details are applied after chaos, so user choices always win:

```yaml
---
enabled: true
preset: dog
chaos: true
seed: 1234
details:
  embodiment: robot
  role: detective
  world: noir
---
```

`embodiment` and `species` are independent. A robot dog is therefore `embodiment: robot` plus `species: dog`.

## Free-form nuance

The host LLM may preserve requested nuance that is not represented by catalog axes:

```yaml
custom:
  display_name: 냉소적인 우주 해적 고양이
  address_user_as: 선장
  rules: 해적선 비유를 사용한다 | 건조한 농담을 제한적으로 사용한다
```

`custom` accepts only `display_name`, `address_user_as`, and pipe-separated `rules`. The compiler limits their size. Safety and accuracy remain higher priority than custom rules.

Legacy `character`, `advanced`, `overrides`, and `form` remain accepted as aliases for `preset`, `details`, and `embodiment`.
