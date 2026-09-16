// `check_math_loading/readouts.js`: readouts are judged against the frozen targets for both
// angle and direction sliders, and dormant saved-font variants are ignored.
import assert from "node:assert/strict";
import { probe } from "../probe.mjs";

const sans = {
  /** @param {string} selector */
  closest: (selector) => (selector.includes("kpress-math-face") ? {} : null),
};
const dormant = { dataset: { squaresMathContexts: "system-sans" }, parentElement: null };
/** @param {string} text */
const output = (text) => ({
  /** @param {string} selector */
  querySelectorAll: (selector) =>
    selector === ".katex"
      ? [{ closest: () => dormant }, sans]
      : [
          { textContent: "stale dormant source", closest: () => dormant },
          { textContent: text, closest: () => null },
        ],
});
/** @type {Record<string, object>} */
const elements = {
  "phi-example": { value: "196" },
  "kslider-example": { value: "123", getAttribute: () => "Direction 123 of 448" },
  "s-phi-example": output("19.600^{\\circ}"),
  "kval-example": output("k = 123"),
};
Object.assign(globalThis, {
  document: {
    /** @param {string} id */
    getElementById: (id) => elements[id],
    documentElement: { dataset: {} },
  },
});
const targets = [
  { id: "phi-example", value: "412" },
  { id: "kslider-example", value: "7" },
];

const math = probe("devtools/probes/math/library.js")();
/** @type {{ expected_source: string, actual_value: string, source: string, state_matches: boolean, sans: boolean, supported: boolean }[]} */
const readouts = probe("devtools/probes/check_math_loading/readouts.js")({ targets, math });
const [angle, direction] = /** @type {[(typeof readouts)[number], (typeof readouts)[number]]} */ (
  readouts
);
assert.equal(angle.expected_source, "41.200^{\\circ}");
assert.equal(angle.actual_value, "196");
assert.equal(angle.source, "19.600^{\\circ}");
assert.equal(direction.expected_source, "k = 7");
assert.equal(direction.actual_value, "123");
assert.equal(direction.source, "k = 123");
assert.equal(direction.state_matches, false);
assert.ok(readouts.every((readout) => readout.sans && readout.supported));
