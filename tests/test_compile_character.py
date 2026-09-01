import importlib.util
import json
import random
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).parents[1]
SCRIPT = ROOT / "plugins/with-character/scripts/compile_character.py"
CATALOG = ROOT / "plugins/with-character/scripts/catalog.json"
spec = importlib.util.spec_from_file_location("compiler", SCRIPT)
compiler = importlib.util.module_from_spec(spec)
spec.loader.exec_module(compiler)


class CompilerTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.catalog = json.loads(CATALOG.read_text(encoding="utf-8"))

    def parse(self, body):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "config.md"
            path.write_text(body, encoding="utf-8")
            return compiler.parse_config(path)

    def resolve(self, config):
        return compiler.resolve(config, self.catalog, rng=random.Random(7))

    def test_missing_config_keeps_style_disabled(self):
        result = self.resolve({})
        self.assertFalse(result["enabled"])

    def test_simple_dog_config_enables_subtitle_default(self):
        result = self.resolve({"character": "dog"})
        self.assertTrue(result["enabled"])
        self.assertEqual("subtitle", result["mode"])
        self.assertEqual("dog", result["language"])

    def test_simple_config_file_is_parsed(self):
        config = self.parse("---\nenabled: true\ncharacter: dog\nmode: reaction\n---\n")
        result = self.resolve(config)
        self.assertEqual("dog", result["character"])
        self.assertEqual("reaction", result["mode"])

    def test_korean_alias_is_supported(self):
        result = self.resolve({"character": "오랑우탄", "mode": "pure"})
        self.assertEqual("orangutan", result["character"])
        self.assertEqual("pure", result["mode"])

    def test_subtitle_prompt_requires_language_and_translation(self):
        result = self.resolve({"character": "dog", "mode": "subtitle"})
        prompt = compiler.prompt(result, Path("/skill"), self.catalog)
        self.assertIn("only the selected character language", prompt)
        self.assertIn("(통역: ...)", prompt)
        self.assertIn("꼬리 흔들기", prompt)

    def test_pure_prompt_forbids_translation_but_preserves_code(self):
        result = self.resolve({"character": "orangutan", "mode": "pure"})
        prompt = compiler.prompt(result, Path("/skill"), self.catalog)
        self.assertIn("do not add a translation", prompt)
        self.assertIn("preserved code", prompt)
        self.assertIn("바나나 내려놓기", prompt)

    def test_reaction_mode_keeps_normal_korean(self):
        result = self.resolve({"character": "dog", "mode": "reaction"})
        prompt = compiler.prompt(result, Path("/skill"), self.catalog)
        self.assertIn("normal Korean", prompt)

    def test_ordinary_character_rejects_pure_mode(self):
        with self.assertRaisesRegex(ValueError, "does not support mode pure"):
            self.resolve({"character": "robot-butler", "mode": "pure"})

    def test_random_comedy_stays_inside_pack(self):
        result = self.resolve({"character": "random", "pack": "comedy"})
        self.assertIn(result["character"], self.catalog["packs"]["comedy"])

    def test_random_pack_filters_by_requested_mode(self):
        result = self.resolve({"character": "random", "pack": "animal", "mode": "pure"})
        self.assertIn(result["character"], {"dog", "orangutan"})

    def test_random_pack_rejects_unsupported_mode(self):
        with self.assertRaisesRegex(ValueError, "has no character supporting mode pure"):
            self.resolve({"character": "random", "pack": "fantasy", "mode": "pure"})

    def test_legacy_preset_and_overrides_remain_supported(self):
        result = self.resolve({"preset": "robot-butler", "overrides": {"personality": "tsundere"}})
        self.assertEqual("robot-butler", result["character"])
        self.assertEqual("tsundere", result["traits"]["personality"])

    def test_advanced_values_are_validated(self):
        with self.assertRaisesRegex(ValueError, "unknown world"):
            self.resolve({"character": "dog", "advanced": {"world": "office-fantasy"}})

    def test_characters_have_valid_unique_combinations(self):
        required = {"form", "identity", "role", "personality", "world", "voice", "relation", "humor"}
        combinations = []
        for name, definition in self.catalog["characters"].items():
            traits = definition["traits"]
            self.assertTrue(required.issubset(traits), name)
            for axis, value in traits.items():
                self.assertIn(value, self.catalog["axes"][axis], f"{name}:{axis}")
            combinations.append(tuple(sorted(traits.items())))
        self.assertEqual(len(combinations), len(set(combinations)))

    def test_language_vocabularies_do_not_overlap_core_sounds(self):
        dog = set(sum(self.catalog["language_profiles"]["dog"]["sounds"].values(), []))
        orangutan = set(sum(self.catalog["language_profiles"]["orangutan"]["sounds"].values(), []))
        self.assertTrue(dog.isdisjoint(orangutan))


if __name__ == "__main__":
    unittest.main()
