#!/usr/bin/env python3
"""Resolve a With Character config into a compact prompt fragment."""
import argparse
import json
from pathlib import Path

AXIS_ORDER = ["form", "identity", "species", "role", "personality", "world", "voice", "relation"]


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


def resolve(config: dict, catalog: dict) -> dict:
    preset = config.get("preset", catalog["defaults"]["preset"])
    if preset not in catalog["presets"]:
        raise ValueError(f"unknown preset: {preset}")
    resolved = dict(catalog["presets"][preset])
    for axis, value in config.get("overrides", {}).items():
        if axis not in catalog["axes"]:
            raise ValueError(f"unknown axis: {axis}")
        if value not in catalog["axes"][axis]:
            raise ValueError(f"unknown {axis}: {value}")
        resolved[axis] = value
    if resolved.get("form") != "animal":
        resolved.pop("species", None)
    intensity = config.get("intensity", catalog["defaults"]["intensity"])
    if intensity not in catalog["intensities"]:
        raise ValueError(f"unknown intensity: {intensity}")
    return {
        "enabled": str(config.get("enabled", "true")).lower() not in {"false", "off", "끄기"},
        "preset": preset,
        "intensity": intensity,
        "traits": resolved,
    }


def prompt(spec: dict, skill_dir: Path) -> str:
    traits = ", ".join(f"{key}={spec['traits'][key]}" for key in AXIS_ORDER if key in spec["traits"])
    return (
        "[With Character ON] Follow " + str(skill_dir / "SKILL.md") + ". "
        f"Resolved character: {traits}. Intensity={spec['intensity']}. "
        "Read references/traits.md only for the selected trait entries. "
        "Priority: accuracy/safety > role > voice > relation > personality > form > world > decorations. "
        "Preserve code, commands, paths, URLs, identifiers, logs, quoted errors, facts, and uncertainty."
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
        print(prompt(spec, args.skill_dir))


if __name__ == "__main__":
    main()
