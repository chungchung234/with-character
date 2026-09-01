import test from "node:test";
import assert from "node:assert/strict";
import { readFileSync, mkdtempSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join, resolve } from "node:path";
import { buildPrompt, freezeConfig, parseConfig, resolveCharacter } from "../plugins/with-character/scripts/compile_character.mjs";

const root = resolve(import.meta.dirname, "..");
const catalog = JSON.parse(readFileSync(join(root, "plugins/with-character/scripts/catalog.json"), "utf8"));

test("resolves an English preset without Python", () => {
  const spec = resolveCharacter({ schema_version: "1", enabled: "true", locale: "en", preset: "anime-cool-rival" }, catalog);
  assert.equal(spec.locale, "en");
  assert.equal(spec.preset, "anime-cool-rival");
  const prompt = buildPrompt(spec, join(root, "plugins/with-character/skills/with-character"), catalog);
  assert.match(prompt, /Locale=en/);
  assert.match(prompt, /natural English/);
});

test("defaults legacy configuration to Korean", () => {
  assert.equal(resolveCharacter({ preset: "dog" }, catalog).locale, "ko");
});

test("rejects an unknown locale", () => {
  assert.throws(() => resolveCharacter({ preset: "dog", locale: "fr" }, catalog), /unknown locale/);
});

test("seeded chaos is stable", () => {
  const config = { preset: "robot-dog", chaos: "true", seed: "stable", intensity: "moderate" };
  assert.deepEqual(resolveCharacter(config, catalog), resolveCharacter(config, catalog));
});

test("freeze writes schema and seed-compatible data", () => {
  const frozen = freezeConfig({ strategy: "preset-random" }, 42);
  assert.equal(frozen.schema_version, "1");
  assert.equal(frozen.seed, "42");
});

test("parses locale from frontmatter", () => {
  const directory = mkdtempSync(join(tmpdir(), "with-character-"));
  const path = join(directory, "config.md");
  writeFileSync(path, "---\nlocale: en\npreset: dog\n---\n");
  assert.deepEqual(parseConfig(path), { locale: "en", preset: "dog" });
});
