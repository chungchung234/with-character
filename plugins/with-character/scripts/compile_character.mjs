#!/usr/bin/env node
/** Resolve preset, random, chaos, locale, and detail settings into a prompt fragment. */
import { createHash, randomBytes } from "node:crypto";
import { readFileSync, writeFileSync, mkdirSync, renameSync } from "node:fs";
import { dirname, extname, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const AXIS_ORDER = ["embodiment", "identity", "species", "role", "personality", "world", "voice", "relation", "humor"];
const LEGACY_AXES = { form: "embodiment" };
const SCHEMA_VERSION = "1";
const TOP_LEVEL_FIELDS = new Set(["schema_version", "enabled", "strategy", "preset", "character", "pack", "chaos", "mode", "intensity", "seed", "locale", "details", "advanced", "overrides", "custom"]);
const SCRIPT_DIR = dirname(fileURLToPath(import.meta.url));

export function parseConfig(path) {
  const result = {};
  let section = null;
  let text;
  try { text = readFileSync(path, "utf8"); } catch (error) {
    if (error.code === "ENOENT") return result;
    throw error;
  }
  for (const raw of text.split(/\r?\n/)) {
    const line = raw.trim();
    if (!line || line === "---" || line.startsWith("#")) continue;
    if (line.endsWith(":")) {
      section = line.slice(0, -1);
      result[section] ??= {};
      continue;
    }
    const split = line.indexOf(":");
    if (split < 0) continue;
    const key = line.slice(0, split).trim();
    const value = line.slice(split + 1).trim().replace(/^['"]|['"]$/g, "");
    if (section && /^\s/.test(raw)) result[section][key] = value;
    else { section = null; result[key] = value; }
  }
  return result;
}

const asBool = value => ["true", "on", "yes", "1", "켜기"].includes(String(value).toLowerCase());

export function validateConfig(config) {
  const version = String(config.schema_version ?? SCHEMA_VERSION);
  if (version !== SCHEMA_VERSION) throw new Error(`unsupported schema_version: ${version}; expected ${SCHEMA_VERSION}`);
  for (const key of Object.keys(config)) if (!TOP_LEVEL_FIELDS.has(key)) throw new Error(`unknown config field: ${key}`);
  for (const section of ["details", "advanced", "overrides", "custom"])
    if (section in config && (typeof config[section] !== "object" || Array.isArray(config[section]))) throw new Error(`${section} must be a mapping`);
  if (config.locale && !["ko", "en"].includes(config.locale)) throw new Error(`unknown locale: ${config.locale}`);
}

function needsSeed(config) {
  const preset = config.preset ?? config.character;
  return ["preset-random", "chaos-random"].includes(config.strategy) || ["random", "chaos-random", "random-chaos"].includes(preset) || asBool(config.chaos ?? false);
}

export function freezeConfig(config, seed) {
  const frozen = { ...config, schema_version: config.schema_version ?? SCHEMA_VERSION };
  if (needsSeed(frozen) && !("seed" in frozen)) frozen.seed = String(seed ?? randomBytes(4).readUInt32BE());
  return frozen;
}

function yamlConfig(config) {
  const lines = ["---"];
  for (const key of ["schema_version", "enabled", "locale", "strategy", "preset", "character", "pack", "chaos", "mode", "intensity", "seed"])
    if (key in config) lines.push(`${key}: ${config[key]}`);
  for (const section of ["details", "advanced", "overrides", "custom"]) if (config[section] && Object.keys(config[section]).length) {
    lines.push(`${section}:`);
    for (const [key, value] of Object.entries(config[section])) lines.push(`  ${key}: ${value}`);
  }
  return `${lines.join("\n")}\n---\n`;
}

// CPython-compatible Random.seed(str) + MT19937. This preserves 1.0 seeded choices
// after moving the runtime from Python to Node.js.
class PythonRandom {
  constructor(seed) {
    const bytes = Buffer.from(String(seed), "utf8");
    const material = Buffer.concat([bytes, createHash("sha512").update(bytes).digest()]);
    let integer = 0n;
    for (const byte of material) integer = (integer << 8n) | BigInt(byte);
    const key = [];
    do { key.push(Number(integer & 0xffffffffn)); integer >>= 32n; } while (integer > 0n);
    this.mt = new Uint32Array(624); this.index = 624;
    this.mt[0] = 19650218;
    for (let i = 1; i < 624; i++) this.mt[i] = (Math.imul(this.mt[i - 1] ^ (this.mt[i - 1] >>> 30), 1812433253) + i) >>> 0;
    let i = 1, j = 0;
    for (let k = Math.max(624, key.length); k; k--) {
      this.mt[i] = ((this.mt[i] ^ Math.imul(this.mt[i - 1] ^ (this.mt[i - 1] >>> 30), 1664525)) + key[j] + j) >>> 0;
      if (++i >= 624) { this.mt[0] = this.mt[623]; i = 1; }
      if (++j >= key.length) j = 0;
    }
    for (let k = 623; k; k--) {
      this.mt[i] = ((this.mt[i] ^ Math.imul(this.mt[i - 1] ^ (this.mt[i - 1] >>> 30), 1566083941)) - i) >>> 0;
      if (++i >= 624) { this.mt[0] = this.mt[623]; i = 1; }
    }
    this.mt[0] = 0x80000000;
  }
  uint32() {
    if (this.index >= 624) {
      for (let i = 0; i < 624; i++) {
        const y = (this.mt[i] & 0x80000000) | (this.mt[(i + 1) % 624] & 0x7fffffff);
        this.mt[i] = this.mt[(i + 397) % 624] ^ (y >>> 1) ^ ((y & 1) ? 0x9908b0df : 0);
      }
      this.index = 0;
    }
    let y = this.mt[this.index++];
    y ^= y >>> 11; y ^= (y << 7) & 0x9d2c5680; y ^= (y << 15) & 0xefc60000; y ^= y >>> 18;
    return y >>> 0;
  }
  getrandbits(bits) {
    if (bits <= 32) return this.uint32() >>> (32 - bits);
    throw new Error("getrandbits above 32 bits is not needed by this catalog");
  }
  randbelow(n) {
    const bits = Math.floor(Math.log2(n)) + 1;
    let value;
    do { value = this.getrandbits(bits); } while (value >= n);
    return value;
  }
}
class SystemRandom {
  randbelow(n) {
    const limit = Math.floor(0x100000000 / n) * n;
    let value;
    do { value = randomBytes(4).readUInt32BE(); } while (value >= limit);
    return value % n;
  }
}
const seededRng = seed => seed == null ? new SystemRandom() : new PythonRandom(seed);
const choice = (values, rng) => values[rng.randbelow(values.length)];
function sample(values, count, rng) {
  const copy = [...values];
  const result = [];
  for (let i = 0; i < count; i++) {
    const j = rng.randbelow(copy.length - i);
    result.push(copy[j]); copy[j] = copy[copy.length - i - 1];
  }
  return result;
}

const canonicalPreset = (value, catalog) => catalog.aliases?.[value] ?? value;
function choosePreset(config, catalog, rng) {
  let strategy = config.strategy ?? "preset";
  let preset = canonicalPreset(config.preset ?? config.character ?? catalog.defaults.preset, catalog);
  if (preset === "random") strategy = "preset-random";
  if (["chaos-random", "random-chaos"].includes(preset)) strategy = "chaos-random";
  if (strategy === "chaos-random") return [null, strategy];
  if (strategy === "preset-random") {
    const pack = config.pack ?? catalog.defaults.pack;
    if (!catalog.packs[pack]) throw new Error(`unknown pack: ${pack}`);
    let candidates = [...catalog.packs[pack]];
    if (["subtitle", "pure"].includes(config.mode)) candidates = candidates.filter(name => catalog.presets[name].language);
    if (!candidates.length) throw new Error(`pack ${pack} has no preset supporting mode ${config.mode}`);
    preset = choice(candidates, rng);
  }
  if (!catalog.presets[preset]) throw new Error(`unknown preset: ${preset}`);
  return [preset, strategy];
}

function randomTraits(catalog, rng) {
  const traits = Object.fromEntries(Object.entries(catalog.axes).filter(([axis]) => axis !== "species").map(([axis, values]) => [axis, choice(values, rng)]));
  if (choice([true, false], rng)) traits.species = choice(catalog.axes.species, rng);
  return traits;
}
function applyChaos(traits, catalog, rng, intensity) {
  const changed = {};
  for (const axis of sample(catalog.chaos_axes, { light: 1, moderate: 2, full: 4 }[intensity], rng)) {
    const options = catalog.axes[axis].filter(value => value !== traits[axis]);
    if (options.length) traits[axis] = changed[axis] = choice(options, rng);
  }
  return [traits, changed];
}
function applyDetails(traits, language, details, catalog) {
  for (const [rawAxis, value] of Object.entries(details)) {
    const axis = LEGACY_AXES[rawAxis] ?? rawAxis;
    if (axis === "language") {
      if (value === "normal") language = null;
      else if (catalog.language_profiles[value]) language = value;
      else throw new Error(`unknown language: ${value}`);
    } else {
      if (!catalog.axes[axis]) throw new Error(`unknown detail axis: ${rawAxis}`);
      if (!catalog.axes[axis].includes(value)) throw new Error(`unknown ${axis}: ${value}`);
      traits[axis] = value;
    }
  }
  return [traits, language];
}
function applyCustom(signature, custom = {}) {
  const allowed = new Set(["display_name", "address_user_as", "rules"]);
  for (const key of Object.keys(custom)) if (!allowed.has(key)) throw new Error(`unknown custom field: ${key}`);
  const rules = String(custom.rules ?? "").split("|").map(rule => rule.trim()).filter(Boolean);
  if ((custom.display_name?.length ?? 0) > 80) throw new Error("custom display_name is too long");
  if ((custom.address_user_as?.length ?? 0) > 40) throw new Error("custom address_user_as is too long");
  if (rules.length > 8 || rules.some(rule => rule.length > 300)) throw new Error("custom rules exceed limits");
  if (!Object.keys(custom).length) return [signature, null];
  const merged = { ...(signature ?? {}) };
  if (custom.address_user_as) merged.address_user_as = custom.address_user_as;
  merged.rules = [...(merged.rules ?? []), ...rules];
  return [merged, custom.display_name ?? null];
}

export function resolveCharacter(config, catalog, rng = seededRng(config.seed), localeData = null) {
  validateConfig(config);
  const explicitlyConfigured = Object.keys(config).length > 0;
  const intensity = config.intensity ?? catalog.defaults.intensity;
  if (!catalog.intensities.includes(intensity)) throw new Error(`unknown intensity: ${intensity}`);
  let [preset, strategy] = choosePreset(config, catalog, rng);
  let traits, displayName, language, signature, chaosChanges, defaultMode;
  if (strategy === "chaos-random") {
    traits = randomTraits(catalog, rng);
    const languages = Object.keys(catalog.language_profiles);
    language = choice(["subtitle", "pure"].includes(config.mode) ? languages : [null, ...languages], rng);
    displayName = "Full Chaos Mix"; signature = null; chaosChanges = { ...traits }; defaultMode = "reaction";
  } else {
    const definition = catalog.presets[preset];
    traits = { ...definition.traits }; displayName = definition.display_name; language = definition.language ?? null;
    signature = definition.signature ?? null; chaosChanges = {}; defaultMode = definition.default_mode;
    if (asBool(config.chaos ?? false)) [traits, chaosChanges] = applyChaos(traits, catalog, rng, intensity);
  }
  [traits, language] = applyDetails(traits, language, config.details ?? config.advanced ?? config.overrides ?? {}, catalog);
  const mode = config.mode ?? defaultMode;
  if (!catalog.modes.includes(mode)) throw new Error(`unknown mode: ${mode}`);
  if (["subtitle", "pure"].includes(mode) && !language) throw new Error(`mode ${mode} requires a character language`);
  const locale = config.locale === "en" ? "en" : "ko";
  if (locale === "en" && localeData) {
    displayName = localeData.display_names?.[preset] ?? displayName;
    signature = localeData.signatures?.[preset] ?? signature;
  }
  let customName; [signature, customName] = applyCustom(signature, config.custom);
  if (customName) displayName = customName;
  return { enabled: !["false", "off", "끄기"].includes(String(config.enabled ?? explicitlyConfigured).toLowerCase()), locale, strategy, preset, display_name: displayName, mode, intensity, traits, language, signature, chaos_changes: chaosChanges, seed: config.seed ?? null };
}

function modeInstruction(spec, languageProfile) {
  const target = spec.locale === "en" ? "English" : "Korean";
  if (spec.mode === "subtitle") return `Character-spoken prose uses only the selected character language, immediately followed by an italicized ${target} translation containing the complete meaning.`;
  if (spec.mode === "pure") return "All prose uses only the selected character language with no translation; preserved code, commands, paths, URLs, identifiers, logs, and quoted errors remain exact.";
  if (languageProfile) return `Useful prose stays in natural ${target}; use character language only for brief reactions.`;
  return `Write useful prose in natural ${target} using the resolved preset voice.`;
}
export function buildPrompt(spec, skillDir, catalog, localeData = null) {
  const traits = AXIS_ORDER.filter(key => key in spec.traits).map(key => `${key}=${spec.traits[key]}`).join(", ");
  const languageProfile = spec.language ? localeData?.language_profiles?.[spec.language] ?? catalog.language_profiles[spec.language] : null;
  const extras = [];
  if (languageProfile) extras.push(`Language profile=${JSON.stringify(languageProfile)}`);
  if (spec.signature) extras.push(`Preset signature=${JSON.stringify(spec.signature)}`);
  if (spec.chaos_changes && Object.keys(spec.chaos_changes).length) extras.push(`Chaos mutations=${JSON.stringify(spec.chaos_changes)}`);
  return `[With Character ON] Follow ${resolve(skillDir, "SKILL.md")}. Locale=${spec.locale}; strategy=${spec.strategy}; preset=${spec.preset}; character=${spec.display_name}; mode=${spec.mode}; intensity=${spec.intensity}; traits: ${traits}. ${modeInstruction(spec, languageProfile)}${extras.length ? ` ${extras.join(". ")}.` : ""} Priority: accuracy/safety > preserved content > preset signature > speech mode > role > voice > relation > personality > embodiment > world > humor.`;
}

function parseArgs(argv) {
  const options = { catalog: resolve(SCRIPT_DIR, "catalog.json"), skillDir: resolve(SCRIPT_DIR, "../skills/with-character"), json: false, freeze: false };
  for (let i = 0; i < argv.length; i++) {
    const arg = argv[i];
    if (arg === "--catalog") options.catalog = resolve(argv[++i]);
    else if (arg === "--skill-dir") options.skillDir = resolve(argv[++i]);
    else if (arg === "--json") options.json = true;
    else if (arg === "--freeze") options.freeze = true;
    else if (arg.startsWith("-")) throw new Error(`unknown option: ${arg}`);
    else if (!options.config) options.config = resolve(arg);
    else throw new Error(`unexpected argument: ${arg}`);
  }
  if (!options.config) throw new Error("config path is required");
  return options;
}

export function main(argv = process.argv.slice(2)) {
  const options = parseArgs(argv);
  const catalog = JSON.parse(readFileSync(options.catalog, "utf8"));
  let config = parseConfig(options.config);
  if (options.freeze) config = freezeConfig(config);
  const localeData = config.locale === "en" ? JSON.parse(readFileSync(resolve(SCRIPT_DIR, "locales/en.json"), "utf8")) : null;
  const spec = resolveCharacter(config, catalog, undefined, localeData);
  if (options.freeze) {
    mkdirSync(dirname(options.config), { recursive: true });
    const temporary = `${options.config}.tmp`;
    writeFileSync(temporary, yamlConfig(config), "utf8"); renameSync(temporary, options.config);
  }
  if (options.json) process.stdout.write(`${JSON.stringify(spec, null, 2)}\n`);
  else if (spec.enabled) process.stdout.write(`${buildPrompt(spec, options.skillDir, catalog, localeData)}\n`);
}

if (process.argv[1] && resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  try { main(); } catch (error) { process.stderr.write(`compile_character: ${error.message}\n`); process.exitCode = 2; }
}
