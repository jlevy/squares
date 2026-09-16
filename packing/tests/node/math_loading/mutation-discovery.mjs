// `math/library.js`'s `mutatedMath`: a mutation rescans only the formulas it can have changed,
// and a stylesheet edit rescans the whole page.
import assert from "node:assert/strict";
import { probe } from "../probe.mjs";

const first = { id: "first" },
  second = { id: "second" };
let fullScans = 0;
Object.assign(globalThis, {
  document: {
    querySelectorAll() {
      fullScans++;
      return [first, second];
    },
  },
});
/**
 * @param {object | null} [math]
 * @param {object[]} [descendants]
 * @returns {{ nodeType: number, closest: (selector: string) => unknown, querySelectorAll: () => object[] }}
 */
const element = (math = null, descendants = []) => ({
  nodeType: 1,
  closest(selector) {
    return selector === ".katex" ? math : null;
  },
  querySelectorAll() {
    return descendants;
  },
});
const wrapper = element(null, [first]);
const glyph = element(first);
const text = { nodeType: 3, parentElement: glyph };

/** @type {(records?: object[]) => Iterable<object>} */
const affected = probe("devtools/probes/math/library.js")().mutatedMath;

assert.deepEqual([...affected()], [first, second]);
assert.deepEqual([...affected([{ type: "attributes", target: wrapper }])], [first]);
assert.deepEqual([...affected([{ type: "characterData", target: text }])], [first]);
assert.deepEqual(
  [
    ...affected([
      { type: "childList", target: element(), addedNodes: [wrapper, glyph], removedNodes: [] },
    ]),
  ],
  [first],
);
assert.deepEqual([...affected([{ type: "attributes", target: element() }])], []);
assert.equal(fullScans, 1, "unrelated canvas and local formula mutations stay local");
const root = element(null, [first, second]);
assert.deepEqual([...affected([{ type: "attributes", target: root }])], [first, second]);
const stylesheet = element();
stylesheet.closest = (/** @type {string} */ selector) =>
  selector.includes("style") ? stylesheet : null;
assert.deepEqual(
  [...affected([{ type: "characterData", target: { nodeType: 3, parentElement: stylesheet } }])],
  [first, second],
);
assert.equal(fullScans, 2, "stylesheet edits invalidate the complete cascade");
