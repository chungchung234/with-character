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
  assert.throws(() => resolveCharacter({ preset: "dog", locale: "auto" }, catalog), /unknown locale/);
});

test("English locale preserves custom overrides", () => {
  const spec = resolveCharacter({
    locale: "en", preset: "anime-cool-rival",
    custom: { display_name: "Custom Captain", address_user_as: "Commander", rules: "Always mention rollback" }
  }, catalog, undefined, english);
  assert.equal(spec.display_name, "Custom Captain");
  assert.equal(spec.signature.address_user_as, "Commander");
  assert.ok(spec.signature.rules.includes("Always mention rollback"));
  assert.match(spec.signature.rules[0], /higher standard/);
});

test("English character languages use localized profiles", () => {
  for (const preset of ["dog", "orangutan", "caveman"]) {
    const spec = resolveCharacter({ locale: "en", preset }, catalog, undefined, english);
    const prompt = buildPrompt(spec, join(root, "plugins/with-character/skills/with-character"), catalog, english);
    assert.doesNotMatch(prompt, /[가-힣]/, `${preset} prompt should not contain Korean profile text`);
  }
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
  assert.equal(Object.keys(catalog.presets).length, 70);
  for (const [id, definition] of Object.entries(catalog.presets)) {
    assert.ok(catalog.modes.includes(definition.default_mode), id);
    for (const [axis, value] of Object.entries(definition.traits)) assert.ok(catalog.axes[axis].includes(value), `${id}.${axis}`);
  }
  for (const [pack, ids] of Object.entries(catalog.packs)) {
    assert.equal(new Set(ids).size, ids.length, `${pack} contains duplicates`);
    for (const id of ids) assert.ok(catalog.presets[id], `${pack} contains unknown ${id}`);
  }
});

test("iconic archetypes are distinct, localized, and available as a pack", () => {
  const iconic = [
    "fiery-celebrity-chef", "dark-vigilante", "arrogant-genius-inventor",
    "dramatic-football-commentator", "historical-drama-king", "overinvested-home-shopping-host"
  ];
  assert.deepEqual(catalog.packs.iconic, iconic);
  assert.equal(catalog.presets["arrogant-genius-inventor"].traits.role, "inventor");
  assert.equal(catalog.presets["dramatic-football-commentator"].traits.role, "commentator");
  assert.equal(catalog.presets["historical-drama-king"].traits.role, "monarch");
  assert.deepEqual(catalog.random_axes.role, catalog.axes.role.slice(0, 30));
  assert.deepEqual(catalog.random_axes.relation, catalog.axes.relation.slice(0, 8));
  for (const id of iconic) {
    assert.ok(english.display_names[id], `${id} needs an English display name`);
    assert.ok(english.signatures[id], `${id} needs an English signature`);
    assert.ok(catalog.presets[id].signature?.rules?.length >= 3, `${id} needs observable Korean rules`);
  }
});

test("romantic relations validate and curated presets use them deliberately", () => {
  assert.deepEqual(catalog.axes.relation.slice(-3), ["romantic-partner", "crush", "spouse"]);
  assert.equal(catalog.presets["anime-tsundere-girl"].traits.relation, "crush");
  assert.equal(catalog.presets["anime-dandere-girl"].traits.relation, "crush");
  assert.equal(catalog.presets["anime-gentle-bishonen"].traits.relation, "crush");
  assert.equal(catalog.presets["anime-deredere-girl"].traits.relation, "romantic-partner");
  assert.equal(catalog.presets["anime-yandere-girl"].traits.relation, "romantic-partner");
  for (const relation of ["romantic-partner", "crush", "spouse"]) {
    const spec = resolveCharacter({ preset: "veteran-engineer", details: { relation } }, catalog);
    assert.equal(spec.traits.relation, relation);
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
  assert.match(englishReadme, /## 🌐 언어: \*\*English\*\*/);
  assert.match(koreanReadme, /## 🌐 언어: .*\*\*한국어\*\*/);
  for (const command of ["/with-character:set", "/with-character:status", "/with-character:on", "/with-character:off", "/with-character:help"])
    assert.ok(englishReadme.includes(command) && koreanReadme.includes(command), `${command} must appear in both READMEs`);
  for (const id of Object.keys(catalog.presets))
    assert.ok(englishReadme.includes(`\`${id}\``) && koreanReadme.includes(`\`${id}\``), `${id} must appear in both catalogs`);
  for (const fact of ["schema_version", "locale", "Node.js"])
    assert.ok(englishReadme.includes(fact) && koreanReadme.includes(fact), `${fact} must appear in both READMEs`);
  for (const install of ["codex plugin marketplace add chungchung234/with-character", "codex plugin add with-character@personal"])
    assert.ok(englishReadme.includes(install) && koreanReadme.includes(install), `${install} must appear in both READMEs`);
});

test("commands resolve compiler and references from the plugin root", () => {
  const status = readFileSync(join(root, "plugins/with-character/commands/status.md"), "utf8");
  const on = readFileSync(join(root, "plugins/with-character/commands/on.md"), "utf8");
  const skill = readFileSync(join(root, "plugins/with-character/skills/with-character/SKILL.md"), "utf8");
  assert.match(status, /\$\{CLAUDE_PLUGIN_ROOT\}\/scripts\/compile_character\.mjs/);
  assert.match(on, /\$\{CLAUDE_PLUGIN_ROOT\}\/skills\/with-character\/references\/request-resolution\.md/);
  assert.match(skill, /never from the project working directory/);
});

test("Claude manifest and workspace fallback support Code and Cowork", () => {
  const claudeManifest = JSON.parse(readFileSync(join(root, "plugins/with-character/.claude-plugin/plugin.json"), "utf8"));
  const codexManifest = JSON.parse(readFileSync(join(root, "plugins/with-character/.codex-plugin/plugin.json"), "utf8"));
  const hook = readFileSync(join(root, "plugins/with-character/hooks/session-start.sh"), "utf8");
  const setCommand = readFileSync(join(root, "plugins/with-character/commands/set.md"), "utf8");
  assert.equal(claudeManifest.name, "with-character");
  assert.equal(claudeManifest.version, "1.4.0");
  assert.equal(claudeManifest.license, "MIT");
  assert.ok(readFileSync(join(root, "plugins/with-character/LICENSE"), "utf8").startsWith("MIT License"));
  assert.equal(codexManifest.version.split("+")[0], claudeManifest.version);
  assert.match(hook, /CLAUDE_PROJECT_DIR:-\$\{PWD\}/);
  assert.match(setCommand, /mkdir -p/);
  assert.match(setCommand, /CLAUDE_PROJECT_DIR:-\$\{PWD\}/);
});
