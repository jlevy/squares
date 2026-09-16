// `render_explainer_pdf/settled.js`: traced settlement goes through the same three frames and
// the same font and math waits as the untraced one, and reports each phase.
import assert from "node:assert/strict";
import { probe } from "../probe.mjs";

/** @type {string[]} */
const events = [];
let frames = 0;
Object.assign(globalThis, {
  /** @param {() => void} callback */
  requestAnimationFrame: (callback) => {
    frames++;
    callback();
  },
  document: {
    documentElement: {
      get offsetHeight() {
        events.push("layout");
        return 100;
      },
    },
    fonts: {
      get ready() {
        events.push("fonts");
        return Promise.resolve();
      },
    },
  },
  squaresMath: {
    async settled() {
      events.push("math");
    },
  },
});

/** @type {(observe?: (phase: string) => unknown) => Promise<void>} */
const settle = probe("devtools/probes/render_explainer_pdf/settled.js")();
/** @type {string[]} */
const phases = [];
await settle((phase) => phases.push(phase));
assert.equal(frames, 3);
assert.deepEqual(events, ["layout", "math", "fonts", "math"]);
assert.deepEqual(phases, [
  "before-final-frames",
  "final-frame-1",
  "final-frame-2",
  "after-fonts",
  "final-frame-3",
  "settled",
]);
frames = 0;
events.length = 0;
await settle();
assert.equal(frames, 3);
assert.deepEqual(events, ["layout", "math", "fonts", "math"]);
