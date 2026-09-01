import importlib.util
import json
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

    def test_default_is_robot_operator(self):
        result = compiler.resolve({}, self.catalog)
        self.assertEqual("robot-operator", result["preset"])
        self.assertEqual("robot", result["traits"]["form"])

    def test_overrides_are_composed(self):
        config = self.parse("---\npreset: robot-butler\nintensity: full\noverrides:\n  personality: tsundere\n  world: fantasy\n---\n")
        result = compiler.resolve(config, self.catalog)
        self.assertEqual("butler", result["traits"]["role"])
        self.assertEqual("tsundere", result["traits"]["personality"])
        self.assertEqual("fantasy", result["traits"]["world"])

    def test_species_is_removed_from_non_animal_override(self):
        result = compiler.resolve({"preset":"fox-wizard", "overrides":{"form":"robot"}}, self.catalog)
        self.assertNotIn("species", result["traits"])

    def test_unknown_value_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "unknown world"):
            compiler.resolve({"preset":"robot-butler", "overrides":{"world":"office-fantasy"}}, self.catalog)

    def test_unknown_intensity_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "unknown intensity"):
            compiler.resolve({"intensity":"maximum"}, self.catalog)

    def test_presets_have_required_axes_and_valid_values(self):
        required = {"form", "identity", "role", "personality", "world", "voice", "relation"}
        for name, preset in self.catalog["presets"].items():
            self.assertTrue(required.issubset(preset), name)
            for axis, value in preset.items():
                self.assertIn(value, self.catalog["axes"][axis], f"{name}:{axis}")

    def test_presets_resolve_to_unique_combinations(self):
        combinations = []
        for name in self.catalog["presets"]:
            traits = compiler.resolve({"preset": name}, self.catalog)["traits"]
            combinations.append(tuple(sorted(traits.items())))
        self.assertEqual(len(combinations), len(set(combinations)))


if __name__ == "__main__":
    unittest.main()
