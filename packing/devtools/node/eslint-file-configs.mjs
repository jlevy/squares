// The configuration ESLint resolves for each file, as data, for `test_browser_floor_contract.py`.
//
//   git ls-files '*.js' | node eslint-file-configs.mjs <eslint.config.js> [<block.json>]
//
// Reads repository-relative paths, one per line, on standard input, resolved against the working
// directory as ESLint resolves them in the gate. Prints one JSON array: for each path, whether
// ESLint ignores it and, if not, the severity of each rule it applies (0, 1 or 2), the parser's
// name and the parser options. The contract test requires that every owned file is reached and
// that all of them resolve alike, which is what "no file-specific block" means as a fact rather
// than a reading of the config's source.
//
// `<block.json>`, when given, is a configuration object ESLint applies after the config file's
// own. It is how the test proves that a relaxed block, reintroduced, is seen.
import { readFileSync } from "node:fs";
import { resolve } from "node:path";
import { ESLint } from "eslint";

/** @typedef {{ rules?: Record<string, unknown>, languageOptions?: { parser?: { meta?: { name?: string } }, parserOptions?: unknown } }} Resolved */

const SEVERITIES = new Map([
  ["off", 0],
  ["warn", 1],
  ["error", 2],
]);

/**
 * @param {unknown} setting
 * @returns {number}
 */
function severity(setting) {
  const level = Array.isArray(setting) ? /** @type {unknown} */ (setting[0]) : setting;
  if (typeof level === "number") {
    return level;
  }
  const named = typeof level === "string" ? SEVERITIES.get(level) : undefined;
  if (named === undefined) {
    throw new Error(`unrecognised rule setting: ${JSON.stringify(setting)}`);
  }
  return named;
}

const [configPath, blockPath] = process.argv.slice(2);
if (configPath === undefined) {
  throw new Error("usage: eslint-file-configs.mjs <eslint.config.js> [<block.json>] < paths");
}
const eslint = new ESLint({
  overrideConfigFile: resolve(configPath),
  ...(blockPath === undefined
    ? {}
    : { overrideConfig: /** @type {object} */ (JSON.parse(readFileSync(blockPath, "utf8"))) }),
});

const paths = readFileSync(0, "utf8")
  .split("\n")
  .filter((line) => line !== "");
/** @type {Array<{ path: string, ignored: boolean, rules?: Record<string, number>, parser?: string | null, parserOptions?: unknown }>} */
const files = [];
for (const path of paths) {
  if (await eslint.isPathIgnored(path)) {
    files.push({ path, ignored: true });
    continue;
  }
  const resolved = /** @type {Resolved | undefined} */ (await eslint.calculateConfigForFile(path));
  files.push({
    path,
    ignored: false,
    rules: Object.fromEntries(
      Object.entries(resolved?.rules ?? {}).map(([rule, setting]) => [rule, severity(setting)]),
    ),
    parser: resolved?.languageOptions?.parser?.meta?.name ?? null,
    parserOptions: resolved?.languageOptions?.parserOptions ?? null,
  });
}
process.stdout.write(JSON.stringify(files));
