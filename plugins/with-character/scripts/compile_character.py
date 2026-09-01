#!/usr/bin/env python3
"""Resolve a simple With Character config into a compact prompt fragment."""
import argparse
import json
import random
from pathlib import Path
from typing import Optional

AXIS_ORDER = ["form", "identity", "species", "role", "personality", "world", "voice", "relation", "humor"]


def parse_config(path: Path) -> dict:
    result, section = {}, None
    if not path.exists():
        return result
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line == "---" or line.startswith("#"):
            continue
        if line.endswith(":"):
            section = line[:-1]
            result.setdefault(section, {})
            continue
        if ":" not in line:
            continue
        key, value = (part.strip() for part in line.split(":", 1))
        value = value.strip("'\"")
        if section and raw[:1].isspace():
            result[section][key] = value
        else:
            section = None
            result[key] = value
    return result


def canonical_character(value: str, catalog: dict) -> str:
    return catalog.get("aliases", {}).get(value, value)


def resolve(config: dict, catalog: dict, rng=None) -> dict:
    rng = rng or random.SystemRandom()
    explicitly_configured = bool(config)
    character = canonical_character(config.get("character", config.get("preset", catalog["defaults"]["character"])), catalog)
    pack = config.get("pack", "comedy")
    if character == "random":
        if pack not in catalog["packs"]:
            raise ValueError(f"unknown pack: {pack}")
        candidates = catalog["packs"][pack]
        requested_mode = config.get("mode")
        if requested_mode:
            candidates = [name for name in candidates if requested_mode in catalog["characters"][name]["supported_modes"]]
            if not candidates:
                raise ValueError(f"pack {pack} has no character supporting mode {requested_mode}")
        character = rng.choice(candidates)
    if character not in catalog["characters"]:
        raise ValueError(f"unknown character: {character}")

    definition = catalog["characters"][character]
    mode = config.get("mode", definition["default_mode"])
    if mode not in catalog["modes"]:
        raise ValueError(f"unknown mode: {mode}")
    if mode not in definition["supported_modes"]:
        supported = ", ".join(definition["supported_modes"])
        raise ValueError(f"{character} does not support mode {mode}; choose: {supported}")

    resolved = dict(definition["traits"])
    advanced = config.get("advanced", config.get("overrides", {}))
    for axis, value in advanced.items():
        if axis not in catalog["axes"]:
            raise ValueError(f"unknown advanced axis: {axis}")
        if value not in catalog["axes"][axis]:
            raise ValueError(f"unknown {axis}: {value}")
        resolved[axis] = value
    if resolved.get("form") != "animal":
        resolved.pop("species", None)

    intensity = config.get("intensity", catalog["defaults"]["intensity"])
    if intensity not in catalog["intensities"]:
        raise ValueError(f"unknown intensity: {intensity}")
    enabled_default = explicitly_configured
    enabled = str(config.get("enabled", enabled_default)).lower() not in {"false", "off", "끄기"}
    language_id = definition.get("language")
    return {
        "enabled": enabled,
        "character": character,
        "display_name": definition["display_name"],
        "mode": mode,
        "intensity": intensity,
        "traits": resolved,
        "language": language_id
    }


def mode_instruction(spec: dict, language_profile: Optional[dict]) -> str:
    if spec["mode"] == "subtitle":
        return (
            "Every character-spoken prose line must use only the selected character language, followed immediately "
            "by an italicized Korean '(통역: ...)' line containing the complete useful meaning."
        )
    if spec["mode"] == "pure":
        return (
            "All explanatory and conversational prose must use only the selected character language; do not add a translation. "
            "This intentionally sacrifices prose utility, but preserved code, commands, paths, URLs, identifiers, logs, and quoted errors remain exact."
        )
    if language_profile:
        return (
            "Write the useful explanation in normal Korean and use the selected character language only for brief reactions "
            "at openings, transitions, or endings."
        )
    return "Write useful prose in the resolved character voice; reaction mode does not alter preserved content."


def prompt(spec: dict, skill_dir: Path, catalog: dict) -> str:
    traits = ", ".join(f"{key}={spec['traits'][key]}" for key in AXIS_ORDER if key in spec["traits"])
    language_profile = catalog["language_profiles"].get(spec["language"]) if spec["language"] else None
    language = ""
    if language_profile:
        language = " Language profile=" + json.dumps(language_profile, ensure_ascii=False, separators=(",", ":")) + "."
    return (
        "[With Character ON] Follow " + str(skill_dir / "SKILL.md") + ". "
        f"Character={spec['character']} ({spec['display_name']}); mode={spec['mode']}; intensity={spec['intensity']}; traits: {traits}. "
        + mode_instruction(spec, language_profile) + language + " "
        "Priority: accuracy/safety > preserved content > speech mode > role > voice > relation > personality > form > world > humor."
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("config", type=Path)
    parser.add_argument("--catalog", type=Path, default=Path(__file__).with_name("catalog.json"))
    parser.add_argument("--skill-dir", type=Path, default=Path(__file__).parents[1] / "skills" / "with-character")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    catalog = json.loads(args.catalog.read_text(encoding="utf-8"))
    try:
        spec = resolve(parse_config(args.config), catalog)
    except ValueError as error:
        parser.error(str(error))
    if args.json:
        print(json.dumps(spec, ensure_ascii=False, indent=2))
    elif spec["enabled"]:
        print(prompt(spec, args.skill_dir, catalog))


if __name__ == "__main__":
    main()
