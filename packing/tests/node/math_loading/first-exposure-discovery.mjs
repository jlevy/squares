// `check_math_loading/first_paint.js`: discovery at install never requests the fonts of a
// dormant saved-font variant, and never asks a hidden staging node whether it is visible.
import assert from "node:assert/strict";
import { probe } from "../probe.mjs";

/** @type {string[]} */
const checked = [];
/** @param {string} contexts */
const variant = (contexts) => ({ dataset: { squaresMathContexts: contexts }, parentElement: null });
/**
 * @param {string} id
 * @param {string} [contexts]
 */
const formula = (id, contexts) => ({
  id,
  closest: () => (contexts ? variant(contexts) : null),
  checkVisibility() {
    throw new Error("discovery must preserve hidden staging");
  },
});
const maths = [
  formula("plain-hidden-certificate"),
  formula("selected", "custom-serif"),
  formula("dormant", "custom-sans"),
];
Object.assign(globalThis, {
  document: { documentElement: { dataset: {} }, querySelectorAll: () => maths },
  MutationObserver: class {
    observe() {}
  },
  requestAnimationFrame: () => {},
});

const library = probe("devtools/probes/math/library.js")();
Object.assign(globalThis, {
  __squaresMathProbes: {
    ...library,
    /** @param {{ id: string }} math */
    requiredFonts: (math) => {
      checked.push(math.id);
      return [];
    },
  },
});
probe("devtools/probes/check_math_loading/first_paint.js")();
assert.deepEqual(checked, ["plain-hidden-certificate", "selected"]);
