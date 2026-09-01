<div align="center">

**English** · [한국어](README.ko.md)

# With Character

**Give your coding agent a personality without changing the code or the facts.**

64 curated characters · Korean and English · preset random · Chaos remix

[![Claude Code Plugin](https://img.shields.io/badge/Claude_Code-plugin-D97757?style=flat-square)](https://code.claude.com/docs/en/plugins)
[![Codex Skill](https://img.shields.io/badge/Codex-skill-111111?style=flat-square)](https://github.com/openai/codex)
[![Runtime](https://img.shields.io/badge/runtime-Node.js-339933?style=flat-square)](#requirements)
[![License](https://img.shields.io/badge/license-MIT-blue?style=flat-square)](LICENSE)

[Quick start](#quick-start) · [Characters](#character-packs) · [Random & Chaos](#random-and-chaos) · [Configuration](#configuration)

</div>

With Character is a Claude Code plugin and Codex skill that changes conversational voice, relationship, world, and reactions while preserving technical accuracy. Pick a polished preset, ask for a random character, remix one with Chaos, or describe a custom persona in natural English or Korean.

```text
You: I found the null error on line 42.

Cool Rival: Not a bad find. Now prove what caused it.
Dog:        Woof! Sniff… woof! (Translation: You found the null on line 42. Let's trace it!)
Gangster Bro: Boss!!! That nasty null was hiding on line 42!!!
```

> Character styling never rewrites code blocks, commands, file paths, URLs, identifiers, logs, or quoted errors. Accuracy and safety always outrank role-play.

## Quick start

```text
/plugin marketplace add chungchung234/with-character
/plugin install with-character@with-character
/with-character:set cool rival in English
```

The selected configuration is saved to `.claude/with-character.local.md` and applies immediately. Installation alone does not force a character voice.

```text
/with-character:status
/with-character:off
/with-character:on
```

Natural-language selection is handled by the host LLM, not a brittle keyword parser:

```text
/with-character:set cheerful tutor
/with-character:set a robot dog who talks like a detective
/with-character:set random fantasy preset in English
/with-character:set full chaos random
```

## Character packs

There are 64 complete presets. IDs remain language-neutral, so the same saved configuration works in either locale.

| Pack | Examples |
|---|---|
| Anime girls | Tsundere, Deredere, Kuudere, Dandere, Genki, Yandere, Oneesan, Ojou-sama, Neko, Kusogaki |
| Anime characters | Shonen Hero, Cool Rival, Delinquent Senpai, Gentle Bishonen, Genius Strategist, Hot-blooded Captain, Mysterious Mentor |
| Fantasy | Dragon Sage, Elf Ranger, Dwarf Smith, Slime Merchant, Necromancer Scholar, Holy Paladin, Bard, Rogue, Druid, Warlock |
| Science fiction | Space Captain, Cyberpunk Hacker, Android Medic, Alien Researcher, Space Marine, Bounty Hunter, Starship Engineer, Synthetic Detective |
| Professional | Clinical Diagnostician, Strict Coach, Cheerful Tutor, Veteran Engineer, Chef Mentor, Gentleman Detective |
| Animal & comedy | Dog, Bark-only Dog, Robot Dog, Orangutan, Wild Orangutan, Caveman Developer, Gangster Bro |

Use `/with-character:help` for guidance, or browse the complete preset definitions in [`catalog.json`](plugins/with-character/scripts/catalog.json).

## Random and Chaos

Random chooses one curated preset. Chaos starts from a recognizable preset and mutates a few traits. Chaos Random generates a full combination across all axes.

```text
/with-character:set random
/with-character:set random from the sci-fi pack
/with-character:set robot dog with chaos
/with-character:set full chaos random
```

Funny but usable remixes include a robot dog detective from a noir world, a tsundere dragon code reviewer, an orangutan space captain with subtitles, or a caveman security mentor. A seed is written when randomization is used, keeping the result stable across sessions.

## Speech modes

| Mode | Behavior |
|---|---|
| `reaction` | Useful prose stays in the configured locale; character sounds appear only as short reactions. |
| `subtitle` | Character language is followed by a complete translation in the configured locale. |
| `pure` | All prose uses the character language; exact technical content is still preserved. |

`pure` is intentionally chaotic. Prefer `reaction` or `subtitle` for detailed technical explanations.

## Configuration

```yaml
---
schema_version: 1
enabled: true
locale: en
preset: anime-cool-rival
---
```

An advanced remix can override individual axes:

```yaml
---
schema_version: 1
enabled: true
locale: en
preset: dog
chaos: true
intensity: moderate
details:
  embodiment: robot
  role: detective
  world: noir
---
```

Supported locales are `ko` and `en`. Existing configurations without `locale` remain Korean for backward compatibility. Natural-language `/set` requests store the request language automatically; an explicit language request takes priority.

## Requirements

- Claude Code plugin support or a Codex-compatible skill loader
- Node.js available as `node`
- No Python installation and no third-party npm package required at runtime

The session hook injects only the resolved character specification—not both language catalogs—so English support adds negligible prompt overhead.

## Development

```bash
node --test tests/test_compile_character.mjs
node plugins/with-character/scripts/compile_character.mjs examples/basic.md --json
```

The Python compiler remains only as a 1.0 compatibility reference; plugin execution no longer calls it.

## License

[MIT](LICENSE)
