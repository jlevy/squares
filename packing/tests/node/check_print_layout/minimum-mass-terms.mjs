// `check_print_layout/active_math_text.js`: the minimum mass is read from the selected
// profile's semantic fraction only. Clipped active MathML survives, dormant font variants
// cannot add terms, and a wrong active term stays observable to the certificate comparison.
import assert from "node:assert/strict";
import { probe } from "../probe.mjs";

/** @type {Record<string, string>} */
const dataset = {};
Object.assign(globalThis, { document: { documentElement: { dataset } } });
/**
 * @param {string} contexts
 * @param {string} textContent
 */
const make = (contexts, textContent) => ({
  textContent,
  closest: () => ({ dataset: { squaresMathContexts: contexts }, parentElement: null }),
});
const nodes = [
  make("custom-serif custom-sans", "7"),
  make("custom-serif custom-sans", "8"),
  make("system-serif system-sans", "9"),
  make("system-serif system-sans", "10"),
];

const math = probe("devtools/probes/math/library.js")();
/** @type {(nodes: object[], o: { math: object }) => string[]} */
const activeMathText = probe("devtools/probes/check_print_layout/active_math_text.js");
/** @param {object[]} matched */
const terms = (matched) => activeMathText(matched, { math });

for (const prose of ["serif", "sans"]) {
  dataset.kpressProseFont = prose;
  dataset.kpressFontSet = "custom";
  assert.deepEqual(terms(nodes), ["7", "8"]);
  dataset.kpressFontSet = "system";
  assert.deepEqual(terms(nodes), ["9", "10"]);
}
// Wrong active content must remain observable to the certificate comparison.
/** @type {{ textContent: string }} */ (nodes[2]).textContent = "999";
assert.deepEqual(terms(nodes), ["999", "10"]);
