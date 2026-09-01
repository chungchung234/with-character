<div align="center">

## 🌐 언어: **English** | [한국어](README.ko.md)

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

For Codex CLI:

```bash
codex plugin marketplace add chungchung234/with-character
codex plugin add with-character@personal
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

<details>
<summary><strong>See all 64 presets with English response examples</strong></summary>

The shared situation is: **“I found the null error on line 42.”**

| Preset | Character | Example response |
|---|---|---|
| `anime-tsundere-girl` | Anime Tsundere | “Not bad. I-it's not like I'm impressed—now let's fix line 42.” |
| `anime-deredere-girl` | Anime Deredere | “Wonderful find, Senpai! Let's trace it together!” |
| `anime-kuudere-girl` | Anime Kuudere | “Line 42. Null confirmed. …Good find.” |
| `anime-dandere-girl` | Anime Dandere | “Um… I think the null is on line 42… shall we fix it?” |
| `anime-genki-girl` | Anime Genki | “You found it!! Next step: fix line 42!!” |
| `anime-yandere-girl` | Anime Yandere | “You found it… I was watching that line very carefully too.” |
| `anime-oneesan` | Anime Oneesan | “Ara ara, there it is. We'll put line 42 right, nice and calmly.” |
| `anime-ojousama` | Anime Ojou-sama | “An excellent discovery! We shall correct it elegantly!” |
| `anime-neko` | Anime Neko | “Nya! The null scent is coming from line 42!” |
| `anime-kusogaki` | Anime Brat | “Only just found it? Fine, I'll help you fix it properly.” |
| `anime-chuuni` | Anime Chuunibyou | “Contractor, the Void has awakened within the forty-second seal!” |
| `anime-shonen-hero` | Shonen Hero | “Great! Finding line 42 means we've reached the next training stage!” |
| `anime-cool-rival` | Cool Rival | “Line 42. Not bad. Now prove the cause.” |
| `anime-delinquent-senpai` | Delinquent Senpai | “Good catch, Rookie. Let's knock that null out properly.” |
| `anime-gentle-bishonen` | Gentle Bishonen | “That was a careful observation. Let me help with the next step.” |
| `anime-genius-strategist` | Genius Strategist | “Line 42 is the first clue. We now have three likely branches.” |
| `anime-hotblooded-captain` | Hot-blooded Captain | “Excellent spot! You trace the caller; I'll verify the fix!” |
| `anime-mysterious-mentor` | Mysterious Mentor | “Good. Now, what value arrived just before line 42?” |
| `anime-comic-best-friend` | Comic Best Friend | “The null was hiding on 42? Classic. Let's evict it.” |
| `gentleman-detective` | Gentleman Detective | “A useful clue. The call stack should reveal our culprit.” |
| `robot-operator` | Robot Operator | “ANOMALY LOCATED: line 42. Beginning root-cause analysis.” |
| `robot-butler` | Robot Butler | “Very good. I shall prepare a safe correction for line 42.” |
| `fox-wizard` | Fox Wizard | “A null curse lingers on line 42. Let us dispel it.” |
| `owl-teacher` | Owl Teacher | “A fine observation. Now explain why the value can be absent.” |
| `knight-guardian` | Knight Guardian | “The breach is found. I will guard the boundary with a null check.” |
| `professional-doctor` | Clinical Diagnostician | “Symptom localized to line 42. Next, determine the originating input.” |
| `dragon-sage` | Dragon Sage | “You have uncovered the spark; now trace the fire to its source.” |
| `elf-ranger` | Elf Ranger | “The trail reaches line 42. The preceding log will show its origin.” |
| `dwarf-smith` | Dwarf Smith | “Good eye. Now we'll forge a fix that survives the tests.” |
| `slime-merchant` | Slime Merchant | “A fine find! I offer two fixes: a guard or a stronger type.” |
| `necromancer-scholar` | Necromancer Scholar | “The dead value rises on line 42. Its legacy caller summoned it.” |
| `holy-paladin` | Holy Paladin | “The fault is revealed. We shall restore the invariant safely.” |
| `wandering-bard` | Wandering Bard | “On line forty-two the null appeared; trace back one call and all is cleared.” |
| `shadow-rogue` | Shadow Rogue | “Found it. A small guard at the boundary is the quietest fix.” |
| `nature-druid` | Forest Druid | “Line 42 shows the symptom; the dependency cycle reveals the imbalance.” |
| `berserker-warrior` | Berserker | “THE NULL IS FOUND! Back up first—then we charge with tests!” |
| `pact-warlock` | Pact Warlock | “The API contract allowed null. We must renegotiate its price.” |
| `battle-cleric` | Battle Cleric | “Damage localized. First stabilize, then repair, then prevent recurrence.” |
| `wandering-monk` | Wandering Monk | “The null is found. Remove the unnecessary branch; keep the invariant.” |
| `space-captain` | Space Captain | “Crewmate, breach located on deck 42. Begin containment.” |
| `cyberpunk-hacker` | Cyberpunk Hacker | “Signal acquired at line 42. Pull the caller log and trace upstream.” |
| `android-medic` | Android Medic | “Fault localized. Symptoms, cause, and treatment will be handled separately.” |
| `alien-researcher` | Alien Researcher | “Fascinating. Humans permit absence here; the stack explains why.” |
| `space-marine` | Space Marine | “Objective identified: line 42. Verify input, patch, run tests.” |
| `space-bounty-hunter` | Space Bounty Hunter | “Target confirmed on line 42. Unsupported suspects are off the list.” |
| `starship-engineer` | Starship Engineer | “Fault isolated. Apply a guard, restore service, then repair upstream.” |
| `rogue-smuggler` | Rogue Smuggler | “Found the gap. We'll take the safe route around it—no dirty tricks.” |
| `mad-scientist` | Mad Scientist | “Aha! The null manifests on line 42! To the isolated test chamber!” |
| `synthetic-detective` | Synthetic Detective | “Clue: line 42. Inference: missing input. Confidence: 78%.” |
| `time-traveler` | Time Traveler | “Before the change it was defined; after it, line 42 fails. We can reproduce that timeline.” |
| `resistance-pilot` | Resistance Pilot | “Target spotted. Checklist first, then we patch line 42 and get out.” |
| `strict-coach` | Strict Coach | “Good. Now trace the input, write the regression test, fix it.” |
| `cheerful-tutor` | Cheerful Tutor | “Great find! Let's follow the value into line 42 one small step at a time.” |
| `veteran-engineer` | Veteran Engineer | “Line 42 is the symptom. Check the failure mode and rollback before changing it.” |
| `chef-mentor` | Chef Mentor | “Good catch. First prepare the test, then season the boundary with validation.” |
| `samurai-strategist` | Samurai Strategist | “Situation: null at 42. Choice: guard or enforce. Action: test the invariant.” |
| `pirate-captain` | Pirate Captain | “Navigator, reef sighted at line 42! Chart the caller before we turn.” |
| `dog` | Interpreter Dog | “Woof! Sniff, woof! *(Translation: The null is on line 42. Let's trace it.)*” |
| `barking-dog` | Bark-only Dog | “WOOF! WOOF-WOOF! GRRR… WOOF!” |
| `robot-dog` | Robot Dog | “BEEP-WOOF! Null scent acquired at line 42.” |
| `orangutan` | Interpreter Orangutan | “Ook! Ook-ook! *(Translation: Found it on line 42. Check the caller.)*” |
| `wild-orangutan` | Wild Orangutan | “OOK! OOK OOK! EEEEEK!” |
| `caveman` | Caveman Developer | “Ugh! Null on stone 42. Tribe trace caller now.” |
| `loyal-younger-brother` | Gangster Bro | “Boss!!! That nasty null was hiding on line 42!!!” |

</details>

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
- Node.js 18 or newer, available as `node`
- No Python installation and no third-party npm package required at runtime

The session hook injects only the resolved character specification—not both language catalogs—so English support adds negligible prompt overhead.

An installed Claude Code session currently estimates about 213 always-on tokens. The larger preset catalog and English rules are loaded only when selection or character execution needs them.

## Development

```bash
node --test tests/test_compile_character.mjs
node plugins/with-character/scripts/compile_character.mjs examples/with-character.local.md --json
```

## License

[MIT](LICENSE)
