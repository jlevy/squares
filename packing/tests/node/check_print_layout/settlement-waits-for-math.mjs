// `render_explainer_pdf/settled.js`: two animation frames cannot finish a readout still
// waiting for its font, so settlement waits for the page's pending math as well.
import assert from "node:assert/strict";
import { probe } from "../probe.mjs";

/** @type {(value?: unknown) => void} */
let finish = () => undefined;
const pendingMath = new Promise((resolve) => {
  finish = resolve;
});
Object.assign(globalThis, {
  document: { documentElement: { offsetHeight: 100 }, fonts: { ready: Promise.resolve() } },
  /** @param {() => void} callback */
  requestAnimationFrame: (callback) => queueMicrotask(callback),
  squaresMath: { settled: () => pendingMath },
});
let done = false;

/** @type {() => Promise<void>} */
const settle = probe("devtools/probes/render_explainer_pdf/settled.js")();
const settled = settle().then(() => {
  done = true;
});
// After the microtasks the layout frames run in, and before anything releases the math.
await new Promise((resolve) => setImmediate(resolve));
assert.equal(done, false, "math is still pending after the layout frames");
finish();
await settled;
assert.equal(done, true);
