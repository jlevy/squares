// A probe file's value in this Node process, for the tests that exercise a probe against
// stand-ins rather than a browser.
//
// A probe is one expression, normally an arrow function; this evaluates it the way
// `devtools/node/inspect-probes.mjs` does, wrapped in parentheses with the formatter's
// trailing semicolon trimmed. It runs in this process's own context, so the page globals a
// probe reads (`document`, `getComputedStyle`, `requestAnimationFrame`) resolve to whatever
// the test has put on `globalThis` first, and the values it returns are this realm's, which
// is what `node:assert`'s deep comparisons need.
import { readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { runInThisContext } from "node:vm";

const PACKING = new URL("../../", import.meta.url);

/**
 * The value of the probe at `packing/<path>`.
 *
 * @param {string} path relative to `packing/`, as in `"devtools/probes/math/library.js"`
 * @returns {any} whatever the file evaluates to; each test states the shape it expects
 */
export function probe(path) {
  const file = fileURLToPath(new URL(path, PACKING));
  const source = readFileSync(file, "utf8").trimEnd().replace(/;$/, "");
  return runInThisContext(`(${source}\n)`, { filename: file });
}
