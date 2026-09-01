import test from "node:test";
import assert from "node:assert/strict";
import { readFileSync, mkdtempSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { buildPrompt, freezeConfig, parseConfig, resolveCharacter } from "../plugins/with-character/scripts/compile_character.mjs";

const root = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const catalog = JSON.parse(readFileSync(join(root, "plugins/with-character/scripts/catalog.json"), "utf8"));
const english = JSON.parse(readFileSync(join(root, "plugins/with-character/scripts/locales/en.json"), "utf8"));

test("resolves an English preset without Python", () => {
  const spec = resolveCharacter({ schema_version: "1", enabled: "true", locale: "en", preset: "anime-cool-rival" }, catalog, undefined, english);
  assert.equal(spec.locale, "en");
  assert.equal(spec.preset, "anime-cool-rival");
  assert.equal(spec.display_name, "Cool Rival");
  assert.match(spec.signature.rules[0], /higher standard/);
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

test("preserves Python 1.0 seeded selections", () => {
  const random = resolveCharacter({ strategy: "preset-random", pack: "all", seed: "stable" }, catalog);
  assert.equal(random.preset, "robot-operator");
  const chaos = resolveCharacter({ preset: "robot-dog", chaos: "true", intensity: "moderate", seed: "stable" }, catalog);
  assert.deepEqual(chaos.chaos_changes, { role: "engineer", humor: "slapstick" });
});

test("English locale covers every preset", () => {
  assert.deepEqual(Object.keys(english.display_names).sort(), Object.keys(catalog.presets).sort());
  for (const [id, definition] of Object.entries(catalog.presets)) {
    if (definition.signature) assert.ok(english.signatures[id], `${id} needs an English signature`);
  }
});

test("every preset and pack is valid", () => {
  for (const [id, definition] of Object.entries(catalog.presets)) {
    assert.ok(catalog.modes.includes(definition.default_mode), id);
    for (const [axis, value] of Object.entries(definition.traits)) assert.ok(catalog.axes[axis].includes(value), `${id}.${axis}`);
  }
  for (const [pack, ids] of Object.entries(catalog.packs)) {
    assert.equal(new Set(ids).size, ids.length, `${pack} contains duplicates`);
    for (const id of ids) assert.ok(catalog.presets[id], `${pack} contains unknown ${id}`);
  }
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

test("English and Korean READMEs stay synchronized", () => {
  const englishReadme = readFileSync(join(root, "README.md"), "utf8");
  const koreanReadme = readFileSync(join(root, "README.ko.md"), "utf8");
  assert.match(englishReadme, /\[한국어\]\(README\.ko\.md\)/);
  assert.match(koreanReadme, /\[English\]\(README\.md\)/);
  for (const command of ["/with-character:set", "/with-character:status", "/with-character:on", "/with-character:off", "/with-character:help"])
    assert.ok(englishReadme.includes(command) && koreanReadme.includes(command), `${command} must appear in both READMEs`);
  for (const id of Object.keys(catalog.presets))
    assert.ok(englishReadme.includes(`\`${id}\``) && koreanReadme.includes(`\`${id}\``), `${id} must appear in both catalogs`);
  for (const fact of ["schema_version", "locale", "Node.js"])
    assert.ok(englishReadme.includes(fact) && koreanReadme.includes(fact), `${fact} must appear in both READMEs`);
  for (const install of ["codex plugin marketplace add chungchung234/with-character", "codex plugin add with-character@personal"])
    assert.ok(englishReadme.includes(install) && koreanReadme.includes(install), `${install} must appear in both READMEs`);
});
