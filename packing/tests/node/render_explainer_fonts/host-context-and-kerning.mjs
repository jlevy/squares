// `render_explainer/host_math_init.js`: the host contributes its custom wrappers and TeX
// spacing to the shared math API. The context callback looks through the wrappers without
// turning ordinary prose or a detached node into sans mathematics, and an unrelated pending
// formula does not hold back a completed one. Prints the calls the runtime received.
//
// Usage: node host-context-and-kerning.mjs <MATH_WRAPPERS>
import assert from "node:assert/strict";
import { probe } from "../probe.mjs";

/**
 * @typedef {{ nodeType: number, parentElement: Stand | null, matches: () => boolean,
 *   fontFamily?: string, dataset?: Record<string, string>, querySelectorAll?: () => never[] }} Stand
 * @typedef {{ isSansContext(node: Stand): boolean }} Context
 */

const [wrappers] = process.argv.slice(2);
/** @type {object[]} */
const calls = [];
/** @type {((value?: unknown) => void) | undefined} */
let finish;
/** @type {Stand} */
const sans = {
  nodeType: 1,
  parentElement: null,
  matches: () => false,
  fontFamily: '"Source Sans 3 Variable", sans-serif',
};
const prose = { ...sans, fontFamily: '"PT Serif", serif' };
/**
 * @param {Stand | null} parent
 * @returns {Stand & { dataset: Record<string, string> }}
 */
const wrapper = (parent) => ({
  nodeType: 1,
  parentElement: parent,
  matches: () => true,
  dataset: {},
  querySelectorAll: () => [],
});
const nodes = [wrapper(wrapper(sans)), wrapper(prose), wrapper(null)];
/** @type {(typeof nodes)[number]} */ (nodes[0]).dataset.kpressMathPrepared = "true";
/** @type {{ render: Function, hydrate: Function }} */
const kpressMathText = {
  /**
   * @param {string} source
   * @param {Stand} target
   * @param {{ displayMode: boolean }} options
   * @param {Context} context
   */
  render(source, target, options, context) {
    calls.push({ source, display: options.displayMode, sans: context.isSansContext(target) });
    if (target === nodes[1]) {
      return new Promise((resolve) => {
        finish = resolve;
      });
    }
    return Promise.resolve();
  },
  /**
   * @param {string} source
   * @param {Stand} target
   * @param {{ displayMode: boolean }} options
   * @param {Context} context
   */
  hydrate(source, target, options, context) {
    calls.push({ hydrate: true });
    return Reflect.get(globalThis, "kpressMathText").render(source, target, options, context);
  },
};
Object.assign(globalThis, {
  document: { querySelectorAll: () => nodes, documentElement: { dataset: {} } },
  /** @param {Stand} el */
  getComputedStyle: (el) => ({
    fontFamily: el.fontFamily,
    getPropertyValue: () => '"Source Sans 3 Variable", sans-serif',
  }),
  kpressMathText,
});

probe("devtools/probes/render_explainer/host_math_init.js")(wrappers);
/** @type {{ render(el: Stand, source: string, display: boolean): Promise<boolean>, settled(): Promise<void>, context: Context }} */
const squaresMath = Reflect.get(globalThis, "squaresMath");

assert.deepEqual(nodes.map(squaresMath.context.isSansContext), [true, false, false]);
await squaresMath.render(/** @type {Stand} */ (nodes[0]), "s(11) + cos(x)", true);
const delayed = squaresMath.render(/** @type {Stand} */ (nodes[1]), "n(2)", false);
assert.equal(nodes[0]?.dataset.squaresMathReady, "true");
assert.equal(
  nodes[1]?.dataset.squaresMathReady,
  undefined,
  "an unrelated pending formula does not hide the completed one",
);
let completed = false;
const settled = squaresMath.settled().then(() => {
  completed = true;
});
await Promise.resolve();
assert.equal(completed, false, "initial readouts are still being rendered");
/** @type {() => void} */ (finish)();
await delayed;
await settled;
assert.equal(completed, true);
assert.equal(nodes[1]?.dataset.squaresMathReady, "true");
process.stdout.write(JSON.stringify(calls));
