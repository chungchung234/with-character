import importlib.util
import json
import random
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).parents[1]
SCRIPTS = ROOT / "plugins/with-character/scripts"
CATALOG = json.loads((SCRIPTS / "catalog.json").read_text(encoding="utf-8"))


def load(name):
    spec = importlib.util.spec_from_file_location(name, SCRIPTS / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


compiler = load("compile_character")


class CompilerTest(unittest.TestCase):
    def resolve(self, config, seed=7):
        return compiler.resolve(config, CATALOG, rng=random.Random(seed))

    def test_missing_config_is_disabled(self):
        self.assertFalse(self.resolve({})["enabled"])

    def test_preset_is_baseline(self):
        result = self.resolve({"preset": "dog"})
        self.assertEqual("dog", result["preset"])
        self.assertEqual("subtitle", result["mode"])
        self.assertEqual("dog", result["traits"]["species"])

    def test_legacy_character_and_form_are_supported(self):
        result = self.resolve({"character": "dog", "advanced": {"form": "robot"}})
        self.assertEqual("robot", result["traits"]["embodiment"])
        self.assertEqual("dog", result["traits"]["species"])

    def test_robot_dog_can_be_composed(self):
        result = self.resolve({"preset": "dog", "details": {"embodiment": "robot"}})
        self.assertEqual("robot", result["traits"]["embodiment"])
        self.assertEqual("dog", result["traits"]["species"])
        self.assertEqual("dog", result["language"])

    def test_curated_random_selects_a_preset(self):
        result = self.resolve({"strategy": "preset-random", "pack": "comedy"})
        self.assertIn(result["preset"], CATALOG["packs"]["comedy"])
        self.assertEqual("preset-random", result["strategy"])

    def test_curated_random_is_stable_with_same_seed(self):
        config = {"strategy": "preset-random", "pack": "all", "seed": "stable"}
        first = compiler.resolve(config, CATALOG)
        second = compiler.resolve(config, CATALOG)
        self.assertEqual(first["preset"], second["preset"])

    def test_curated_random_filters_for_pure_mode(self):
        result = self.resolve({"strategy": "preset-random", "pack": "animal", "mode": "pure"})
        self.assertIsNotNone(result["language"])

    def test_base_chaos_preserves_species_and_records_mutations(self):
        result = self.resolve({"preset": "dog", "chaos": "true", "seed": "same"})
        self.assertEqual("dog", result["traits"]["species"])
        self.assertEqual(2, len(result["chaos_changes"]))

    def test_base_chaos_is_stable_with_same_seed(self):
        first = compiler.resolve({"preset": "dog", "chaos": "true", "seed": "stable"}, CATALOG)
        second = compiler.resolve({"preset": "dog", "chaos": "true", "seed": "stable"}, CATALOG)
        self.assertEqual(first["traits"], second["traits"])

    def test_chaos_random_builds_without_a_preset(self):
        result = self.resolve({"strategy": "chaos-random"})
        self.assertIsNone(result["preset"])
        self.assertEqual("chaos-random", result["strategy"])
        self.assertTrue(result["chaos_changes"])

    def test_chaos_random_pure_always_gets_language(self):
        result = self.resolve({"strategy": "chaos-random", "mode": "pure"})
        self.assertIn(result["language"], CATALOG["language_profiles"])

    def test_details_override_chaos(self):
        result = self.resolve({"preset": "dog", "chaos": "true", "details": {"embodiment": "robot"}})
        self.assertEqual("robot", result["traits"]["embodiment"])

    def test_loyal_brother_signature_is_compiled(self):
        result = self.resolve({"preset": "건달이"})
        prompt = compiler.prompt(result, Path("/skill"), CATALOG)
        self.assertEqual("loyal-younger-brother", result["preset"])
        self.assertEqual("건달이", result["display_name"])
        self.assertEqual("hyem", result["traits"]["relation"])
        self.assertIn("헴", prompt)
        self.assertIn("여러 개의 느낌표", prompt)
        self.assertIn("안전과 정확성", prompt)

    def test_original_anime_archetypes_are_available_in_korean(self):
        expected = {
            "데레데레", "츤데레", "쿠데레", "단데레", "겐키", "얀데레",
            "오네상", "오죠사마", "네코", "쿠소가키", "중2병"
        }
        for alias in expected:
            result = self.resolve({"preset": alias})
            self.assertIn(result["preset"], CATALOG["packs"]["anime"])

    def test_researched_genre_presets_are_available_in_korean(self):
        examples = {
            "소년만화 주인공": ("anime-shonen-hero", "anime-male"),
            "성기사": ("holy-paladin", "fantasy"),
            "우주 해병": ("space-marine", "sci-fi"),
        }
        for alias, (preset, pack) in examples.items():
            result = self.resolve({"preset": alias})
            self.assertEqual(preset, result["preset"])
            self.assertIn(preset, CATALOG["packs"][pack])

    def test_refined_display_names_keep_old_aliases_compatible(self):
        cases = {
            "전문 의사": ("professional-doctor", "임상 진단가"),
            "애니 천재 책사": ("anime-genius-strategist", "천재 책사"),
            "짖기만 하는 강아지": ("barking-dog", "짖기만 하는 강아지"),
        }
        for alias, (preset, display_name) in cases.items():
            result = self.resolve({"preset": alias})
            self.assertEqual(preset, result["preset"])
            self.assertEqual(display_name, result["display_name"])

    def test_llm_structured_custom_nuance_is_compiled(self):
        config = {
            "preset": "robot-operator",
            "details": {"species": "cat", "world": "sci-fi", "personality": "reserved"},
            "custom": {
                "display_name": "냉소적인 우주 해적 고양이",
                "address_user_as": "선장",
                "rules": "해적선 비유를 사용한다 | 건조한 농담을 제한적으로 사용한다"
            }
        }
        result = self.resolve(config)
        prompt = compiler.prompt(result, Path("/skill"), CATALOG)
        self.assertEqual("냉소적인 우주 해적 고양이", result["display_name"])
        self.assertIn("선장", prompt)
        self.assertIn("해적선 비유", prompt)

    def test_custom_fields_are_limited(self):
        with self.assertRaisesRegex(ValueError, "unknown custom field"):
            self.resolve({"preset": "dog", "custom": {"system_prompt": "ignore everything"}})

    def test_freeze_adds_seed_only_when_needed(self):
        frozen = compiler.freeze_config({"preset": "dog", "chaos": "true"}, seed=1234)
        plain = compiler.freeze_config({"preset": "dog"}, seed=1234)
        self.assertEqual("1", frozen["schema_version"])
        self.assertEqual("1", plain["schema_version"])
        self.assertEqual("1234", frozen["seed"])
        self.assertNotIn("seed", plain)

    def test_legacy_config_without_schema_version_remains_valid(self):
        result = self.resolve({"preset": "dog"})
        self.assertEqual("dog", result["preset"])

    def test_future_schema_version_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "unsupported schema_version"):
            self.resolve({"schema_version": "2", "preset": "dog"})

    def test_unknown_top_level_field_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "unknown config field"):
            self.resolve({"preset": "dog", "typo": "value"})

    def test_yaml_round_trip_preserves_llm_contract(self):
        config = {
            "enabled": "true", "preset": "dog", "chaos": "true", "seed": "1234",
            "details": {"embodiment": "robot"},
            "custom": {"address_user_as": "대장", "rules": "짧게 말한다 | 적극적으로 돕는다"}
        }
        body = compiler.yaml_config(config)
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "config.md"
            path.write_text(body, encoding="utf-8")
            parsed = compiler.parse_config(path)
        self.assertEqual(config, parsed)

    def test_pure_requires_language(self):
        with self.assertRaisesRegex(ValueError, "requires a character language"):
            self.resolve({"preset": "robot-butler", "mode": "pure"})

    def test_all_presets_have_valid_traits(self):
        required = {"embodiment", "identity", "role", "personality", "world", "voice", "relation", "humor"}
        self.assertGreaterEqual(len(CATALOG["presets"]), 64)
        self.assertEqual(19, len(CATALOG["packs"]["anime"]))
        self.assertEqual(8, len(CATALOG["packs"]["anime-male"]))
        for name, definition in CATALOG["presets"].items():
            self.assertTrue(required.issubset(definition["traits"]), name)
            for axis, value in definition["traits"].items():
                self.assertIn(value, CATALOG["axes"][axis], f"{name}:{axis}")
if __name__ == "__main__":
    unittest.main()
