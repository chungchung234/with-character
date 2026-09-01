# Character configuration

The ordinary user-facing configuration exposes only a character and speech mode:

```yaml
---
character: dog
mode: subtitle
---
```

`mode` may be omitted to use the character default. `dog` and `orangutan` default to `subtitle`; ordinary speaking characters default to `reaction`. A missing config file leaves the style disabled.

Random selection uses a curated pack:

```yaml
---
character: random
pack: comedy
---
```

Advanced customization is optional and hidden from the basic workflow:

```yaml
---
character: robot-butler
mode: reaction
advanced:
  personality: tsundere
  world: fantasy
---
```

Legacy `preset` and `overrides` fields remain accepted as aliases for `character` and `advanced`. Unknown values must be rejected rather than silently invented.
