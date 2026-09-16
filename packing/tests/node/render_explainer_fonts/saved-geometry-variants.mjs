// `render_explainer/host_math_init.js`: only the child prepared for the reader's saved font
// preferences renders, and an older child's failure cannot erase the selected one.
//
// Usage: node saved-geometry-variants.mjs <MATH_WRAPPERS>
import assert from "node:assert/strict";
import { probe } from "../probe.mjs";

/**
 * @typedef {{ nodeType: number, dataset: Record<string, string>, textContent?: string,
 *   parentElement?: Stand, matches: () => boolean, querySelectorAll?: () => Stand[] }} Stand
 */

const [wrappers] = process.argv.slice(2);
const document = { documentElement: { dataset: /** @type {Record<string, string>} */ ({}) } };
/** @type {Stand} */
const parent = {
  nodeType: 1,
  dataset: {},
  textContent: "prepared mathematics",
  matches: () => false,
};
const keys = ["custom-serif", "custom-sans", "system-serif", "system-sans"];
const variants = keys.map((key) => ({
  nodeType: 1,
  parentElement: parent,
  matches: () => true,
  /** @type {Record<string, string>} */
  dataset: { kpressMathPrepared: "true", squaresMathContexts: key },
}));
parent.querySelectorAll = () => variants;
/** @type {string[]} */
const calls = [];
/** @type {((reason?: unknown) => void) | undefined} */
let rejectFirst;
Object.assign(globalThis, {
  document,
  getComputedStyle: () => ({ fontFamily: "serif", getPropertyValue: () => "sans" }),
  kpressMathText: {
    render() {
      throw new Error("matching prepared math must hydrate");
    },
    /**
     * @param {string} _source
     * @param {Stand} target
     */
    hydrate(_source, target) {
      calls.push(/** @type {string} */ (target.dataset.squaresMathContexts));
      if (calls.length === 1) {
        return new Promise((_, reject) => {
          rejectFirst = reject;
        });
      }
      return Promise.resolve();
    },
  },
});

probe("devtools/probes/render_explainer/host_math_init.js")(wrappers);
/** @type {{ render(el: Stand, source: string, display: boolean): Promise<boolean>, settled(): Promise<void> }} */
const squaresMath = Reflect.get(globalThis, "squaresMath");

const old = squaresMath.render(parent, "x", false);
document.documentElement.dataset = { kpressFontSet: "system", kpressProseFont: "sans" };
await squaresMath.render(parent, "y", false);
assert.deepEqual(calls, ["custom-serif", "system-sans"]);
assert.equal(variants[3]?.dataset.squaresMathReady, "true");
assert.equal(variants[1]?.dataset.squaresMathReady, undefined);
assert.equal(variants[2]?.dataset.squaresMathReady, undefined);
/** @type {(reason?: unknown) => void} */ (rejectFirst)(new Error("old profile font failure"));
await old;
await squaresMath.settled();
assert.equal(parent.textContent, "prepared mathematics");
for (const key of keys) {
  const [fontSet, proseFont] = /** @type {[string, string]} */ (key.split("-"));
  document.documentElement.dataset = { kpressFontSet: fontSet, kpressProseFont: proseFont };
  await squaresMath.render(parent, "z", false);
  assert.equal(calls.at(-1), key);
}
