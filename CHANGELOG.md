# Changelog

## 1.4.0

- Expand the curated catalog from 64 to 70 presets with six recognizable but name-independent archetypes.
- Add Fiery Celebrity Chef, Dark Vigilante, Arrogant Genius Inventor, Dramatic Football Commentator, Historical Drama King, and Overinvested Home Shopping Host.
- Add reusable `inventor`, `commentator`, and `monarch` roles plus an `iconic` random pack.
- Keep strong character signatures focused on code and workflow without insulting, coercing, threatening, or misleading the user.

## 1.3.0

- Add `romantic-partner`, `crush`, and `spouse` relationship values with Korean and English natural-language mappings.
- Apply `crush` to Tsundere, Dandere, and Gentle Bishonen; apply `romantic-partner` to Deredere and Yandere.
- Keep romantic relations limited to affectionate address and emotional distance without implying sexual content, control, dependency, or consent.

## 1.2.0

- Add a standard Claude plugin manifest for Claude Cowork and Claude Code discovery.
- Support Cowork workspaces when `CLAUDE_PROJECT_DIR` is unavailable.
- Create workspace configuration directories on first character selection.
- Document Claude Cowork installation and workspace-scoped character settings.

## 1.1.1

- Preserve English `custom` display names, user addresses, and rules by applying custom overrides after locale data.
- Use absolute plugin-root compiler paths in commands and clarify skill-relative path resolution.
- Add localized English dog, orangutan, and caveman language profiles.
- Reject unsupported `locale: auto` instead of silently resolving it to Korean.
- Make trait and character-language references locale-neutral.
- Make the English/Korean README language switcher prominent at the top of both documents.

## 1.1.0

- Remove the Python runtime dependency; the session hook and validator now use Node.js with no third-party packages.
- Add `locale: ko|en` so character responses and subtitle translations work naturally in Korean or English.
- Add an English README and language switch links using the conventional `README.md` / `README.ko.md` layout.
- Keep locale data out of the injected prompt except for the active character, avoiding duplicate catalog context.
- Preserve existing 1.0 seeded choices with a compatible MT19937 implementation in Node.js.
- Add native English names and signature rules for all 64 presets.
- Remove the legacy Python compiler and tests after locking compatibility into the Node suite.

## 1.0.0

- Provide 64 curated character presets across anime, fantasy, science fiction, professional, animal, and comedy packs.
- Support Korean and English natural-language selection, preset random, base Chaos, and full Chaos random.
- Preserve code, commands, paths, logs, quoted errors, facts, and safety above character styling.
- Support stable seeded combinations and `reaction`, `subtitle`, and `pure` speech modes.
- Add configuration schema version 1 while keeping existing unversioned settings compatible.
- Validate unknown configuration fields and reject unsupported future schema versions.
- Keep legacy With Anime Girl names and earlier display names available as aliases.
