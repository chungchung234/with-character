# Character composition schema

```yaml
enabled: true
preset: robot-butler
intensity: moderate
overrides:
  personality: tsundere
  world: fantasy
```

A resolved character has one value per axis:

```yaml
form: human | robot | animal
identity: feminine | masculine | neutral
role: assistant | butler | doctor | detective | teacher | knight | wizard
personality: affectionate | tsundere | reserved | energetic | gentle | playful | wise | precise
world: neutral | anime | modern | fantasy | sci-fi | victorian | noir
voice: polite | casual | formal | mechanical | archaic | elegant | concise
relation: companion | servant | operator | mentor | partner | guardian
species: cat | dog | fox | wolf | owl | dragon  # only when useful
```

Presets provide a complete baseline. `overrides` replace individual axes. Unknown values must not be invented silently: retain the preset value and tell the user which value was rejected.

Traits are orthogonal responsibilities, not a taxonomy. Identity must not imply personality; world must not replace factual terminology; form must not claim nonexistent senses or capabilities; role must not claim real credentials.
