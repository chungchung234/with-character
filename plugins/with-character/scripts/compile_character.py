#!/usr/bin/env python3
"""Resolve preset, random, chaos, and detail settings into a prompt fragment."""
import argparse
import json
import random
import secrets
from pathlib import Path
from typing import Optional

AXIS_ORDER = ["embodiment", "identity", "species", "role", "personality", "world", "voice", "relation", "humor"]
LEGACY_AXES = {"form": "embodiment"}


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


def as_bool(value) -> bool:
    return str(value).lower() in {"true", "on", "yes", "1", "켜기"}


def needs_seed(config: dict) -> bool:
    preset = config.get("preset", config.get("character"))
    strategy = config.get("strategy")
    return strategy in {"preset-random", "chaos-random"} or preset in {"random", "chaos-random", "random-chaos"} or as_bool(config.get("chaos", False))


def freeze_config(config: dict, seed=None) -> dict:
    frozen = dict(config)
    if needs_seed(frozen) and "seed" not in frozen:
        frozen["seed"] = str(seed if seed is not None else secrets.randbits(32))
    return frozen


def yaml_config(config: dict) -> str:
    ordered = ["enabled", "strategy", "preset", "character", "pack", "chaos", "mode", "intensity", "seed"]
    lines = ["---"]
    for key in ordered:
        if key in config:
            lines.append(f"{key}: {config[key]}")
    for section in ["details", "advanced", "overrides", "custom"]:
        if config.get(section):
            lines.append(f"{section}:")
            for key, value in config[section].items():
                lines.append(f"  {key}: {value}")
    lines.append("---")
    return "\n".join(lines) + "\n"


def seeded_rng(config: dict):
    seed = config.get("seed")
    return random.Random(str(seed)) if seed is not None else random.SystemRandom()


def canonical_preset(value: str, catalog: dict) -> str:
    return catalog.get("aliases", {}).get(value, value)


def choose_preset(config: dict, catalog: dict, rng) -> tuple:
    strategy = config.get("strategy", "preset")
    legacy = config.get("character")
    preset = canonical_preset(config.get("preset", legacy or catalog["defaults"]["preset"]), catalog)
    if preset == "random":
        strategy = "preset-random"
    if preset in {"chaos-random", "random-chaos"}:
        strategy = "chaos-random"
    if strategy == "chaos-random":
        return None, strategy
    if strategy == "preset-random":
        pack = config.get("pack", catalog["defaults"]["pack"])
        if pack not in catalog["packs"]:
            raise ValueError(f"unknown pack: {pack}")
        candidates = catalog["packs"][pack]
        requested_mode = config.get("mode")
        if requested_mode in {"subtitle", "pure"}:
            candidates = [name for name in candidates if catalog["presets"][name].get("language")]
            if not candidates:
                raise ValueError(f"pack {pack} has no preset supporting mode {requested_mode}")
        preset = rng.choice(candidates)
    if preset not in catalog["presets"]:
        raise ValueError(f"unknown preset: {preset}")
    return preset, strategy


def random_traits(catalog: dict, rng) -> dict:
    traits = {axis: rng.choice(values) for axis, values in catalog["axes"].items() if axis != "species"}
    if rng.choice([True, False]):
        traits["species"] = rng.choice(catalog["axes"]["species"])
    return traits


def apply_chaos(traits: dict, catalog: dict, rng, intensity: str) -> tuple:
    counts = {"light": 1, "moderate": 2, "full": 4}
    axes = rng.sample(catalog["chaos_axes"], counts[intensity])
    changed = {}
    for axis in axes:
        options = [value for value in catalog["axes"][axis] if value != traits.get(axis)]
        if options:
            value = rng.choice(options)
            traits[axis] = value
            changed[axis] = value
    return traits, changed


def apply_details(traits: dict, language_id: Optional[str], details: dict, catalog: dict) -> tuple:
    for raw_axis, value in details.items():
        axis = LEGACY_AXES.get(raw_axis, raw_axis)
        if axis == "language":
            if value == "normal":
                language_id = None
            elif value in catalog["language_profiles"]:
                language_id = value
            else:
                raise ValueError(f"unknown language: {value}")
            continue
        if axis not in catalog["axes"]:
            raise ValueError(f"unknown detail axis: {raw_axis}")
        if value not in catalog["axes"][axis]:
            raise ValueError(f"unknown {axis}: {value}")
        traits[axis] = value
    return traits, language_id


def apply_custom(signature: Optional[dict], custom: dict) -> tuple:
    if not custom:
        return signature, None
    allowed = {"display_name", "address_user_as", "rules"}
    unknown = set(custom) - allowed
    if unknown:
        raise ValueError(f"unknown custom field: {sorted(unknown)[0]}")
    display_name = custom.get("display_name")
    address = custom.get("address_user_as")
    rules = [rule.strip() for rule in custom.get("rules", "").split("|") if rule.strip()]
    if display_name and len(display_name) > 80:
        raise ValueError("custom display_name is too long")
    if address and len(address) > 40:
        raise ValueError("custom address_user_as is too long")
    if len(rules) > 8 or any(len(rule) > 300 for rule in rules):
        raise ValueError("custom rules exceed limits")
    merged = dict(signature or {})
    if address:
        merged["address_user_as"] = address
    merged["rules"] = list(merged.get("rules", [])) + rules
    return merged or None, display_name


def resolve(config: dict, catalog: dict, rng=None) -> dict:
    rng = rng or seeded_rng(config)
    explicitly_configured = bool(config)
    intensity = config.get("intensity", catalog["defaults"]["intensity"])
    if intensity not in catalog["intensities"]:
        raise ValueError(f"unknown intensity: {intensity}")
    preset, strategy = choose_preset(config, catalog, rng)
    if strategy == "chaos-random":
        traits = random_traits(catalog, rng)
        requested_mode = config.get("mode")
        languages = list(catalog["language_profiles"])
        language_id = rng.choice(languages if requested_mode in {"subtitle", "pure"} else [None] + languages)
        display_name, signature = "완전 카오스 조합", None
        chaos_changes = dict(traits)
        default_mode = "reaction"
    else:
        definition = catalog["presets"][preset]
        traits = dict(definition["traits"])
        display_name = definition["display_name"]
        language_id = definition.get("language")
        signature = definition.get("signature")
        chaos_changes = {}
        default_mode = definition["default_mode"]
        if as_bool(config.get("chaos", False)):
            traits, chaos_changes = apply_chaos(traits, catalog, rng, intensity)

    details = config.get("details", config.get("advanced", config.get("overrides", {})))
    traits, language_id = apply_details(traits, language_id, details, catalog)
    signature, custom_name = apply_custom(signature, config.get("custom", {}))
    if custom_name:
        display_name = custom_name
    mode = config.get("mode", default_mode)
    if mode not in catalog["modes"]:
        raise ValueError(f"unknown mode: {mode}")
    if mode in {"subtitle", "pure"} and not language_id:
        raise ValueError(f"mode {mode} requires a character language")
    enabled = str(config.get("enabled", explicitly_configured)).lower() not in {"false", "off", "끄기"}
    return {
        "enabled": enabled,
        "strategy": strategy,
        "preset": preset,
        "display_name": display_name,
        "mode": mode,
        "intensity": intensity,
        "traits": traits,
        "language": language_id,
        "signature": signature,
        "chaos_changes": chaos_changes,
        "seed": config.get("seed")
    }


def mode_instruction(spec: dict, language_profile: Optional[dict]) -> str:
    if spec["mode"] == "subtitle":
        return "Character-spoken prose uses only the selected language, immediately followed by italicized Korean '(통역: ...)' with the complete meaning."
    if spec["mode"] == "pure":
        return "All prose uses only the selected character language with no translation; preserved code, commands, paths, URLs, identifiers, logs, and quoted errors remain exact."
    if language_profile:
        return "Useful prose stays normal Korean; use character language only for brief reactions."
    return "Write useful prose in the resolved preset voice."


def prompt(spec: dict, skill_dir: Path, catalog: dict) -> str:
    traits = ", ".join(f"{key}={spec['traits'][key]}" for key in AXIS_ORDER if key in spec["traits"])
    language_profile = catalog["language_profiles"].get(spec["language"]) if spec["language"] else None
    extras = []
    if language_profile:
        extras.append("Language profile=" + json.dumps(language_profile, ensure_ascii=False, separators=(",", ":")))
    if spec["signature"]:
        extras.append("Preset signature=" + json.dumps(spec["signature"], ensure_ascii=False, separators=(",", ":")))
    if spec["chaos_changes"]:
        extras.append("Chaos mutations=" + json.dumps(spec["chaos_changes"], ensure_ascii=False, separators=(",", ":")))
    return (
        "[With Character ON] Follow " + str(skill_dir / "SKILL.md") + ". "
        f"Strategy={spec['strategy']}; preset={spec['preset']}; character={spec['display_name']}; mode={spec['mode']}; intensity={spec['intensity']}; traits: {traits}. "
        + mode_instruction(spec, language_profile) + (" " + ". ".join(extras) + "." if extras else "") + " "
        "Priority: accuracy/safety > preserved content > preset signature > speech mode > role > voice > relation > personality > embodiment > world > humor."
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("config", type=Path)
    parser.add_argument("--catalog", type=Path, default=Path(__file__).with_name("catalog.json"))
    parser.add_argument("--skill-dir", type=Path, default=Path(__file__).parents[1] / "skills" / "with-character")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--freeze", action="store_true", help="persist a seed for random or chaos settings")
    args = parser.parse_args()
    catalog = json.loads(args.catalog.read_text(encoding="utf-8"))
    try:
        config = parse_config(args.config)
        if args.freeze:
            config = freeze_config(config)
        spec = resolve(config, catalog)
        if args.freeze:
            args.config.parent.mkdir(parents=True, exist_ok=True)
            temporary = args.config.with_suffix(args.config.suffix + ".tmp")
            temporary.write_text(yaml_config(config), encoding="utf-8")
            temporary.replace(args.config)
    except ValueError as error:
        parser.error(str(error))
    if args.json:
        print(json.dumps(spec, ensure_ascii=False, indent=2))
    elif spec["enabled"]:
        print(prompt(spec, args.skill_dir, catalog))


if __name__ == "__main__":
    main()
