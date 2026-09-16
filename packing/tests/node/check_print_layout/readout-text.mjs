// `check_print_layout/readout_text.js`: a readout's text comes from the active profile. A
// hidden expected value, in a dormant variant or the clipped MathML annotation, cannot mask
// a wrong active readout or replace its glyphs; a fresh client render with no profile
// wrapper and a failed render's raw TeX are read as they are.
import assert from "node:assert/strict";
import { probe } from "../probe.mjs";

/** @type {Record<string, string>} */
const dataset = {};
Object.assign(globalThis, {
  NodeFilter: { SHOW_TEXT: 4 },
  document: {
    documentElement: { dataset },
    /** @param {{ nodes: object[] }} el */
    createTreeWalker: (el) => {
      const nodes = el.nodes[Symbol.iterator]();
      return { nextNode: () => nodes.next().value || null };
    },
  },
});
/**
 * @param {string | null} contexts
 * @param {string} textContent
 * @param {boolean} [semantic]
 */
const make = (contexts, textContent, semantic = false) => ({
  textContent,
  parentElement: {
    /** @param {string} selector */
    closest: (selector) =>
      selector === ".katex-mathml"
        ? semantic
          ? {}
          : null
        : contexts
          ? { dataset: { squaresMathContexts: contexts }, parentElement: null }
          : null,
  },
});
const active = make("custom-serif custom-sans", "wrong visible value");
const readout = {
  nodes: [
    make(null, "direction: "),
    active,
    make("custom-serif custom-sans", "12219313/45000000 30.3836", true),
    make("system-serif system-sans", "12219313/45000000 30.3836"),
  ],
};

const math = probe("devtools/probes/math/library.js")();
/** @type {(el: object, o: { math: object }) => string} */
const readoutText = probe("devtools/probes/check_print_layout/readout_text.js");
/** @param {{ nodes: object[] }} el */
const text = (el) => readoutText(el, { math });

for (const prose of ["serif", "sans"]) {
  dataset.kpressProseFont = prose;
  dataset.kpressFontSet = "custom";
  assert.equal(text(readout), "direction: wrong visible value");
  dataset.kpressFontSet = "system";
  assert.equal(text(readout), "direction: 12219313/45000000 30.3836");
}
// A fresh client render has no profile wrapper; a failed render preserves raw TeX.
assert.equal(text({ nodes: [make(null, "x=2")] }), "x=2");
assert.equal(text({ nodes: [make(null, String.raw`\frac{7}{8}`)] }), String.raw`\frac{7}{8}`);
assert.equal(text({ nodes: [] }), "");
