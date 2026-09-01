# Changelog

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
