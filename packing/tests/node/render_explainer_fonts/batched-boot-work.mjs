// `render_explainer/host_math_init.js`: a decoded formula can finish between batches without
// completing the page early. Queued work and the boot reservation both keep `settled`
// pending, and one browser task submits a bounded number of formulas. Prints `complete`.
//
// Usage: node batched-boot-work.mjs <MATH_WRAPPERS>
import assert from "node:assert/strict";
import { probe } from "../probe.mjs";

/** @typedef {{ index: number, dataset: Record<string, string>, querySelectorAll: () => never[] }} Stand */

const [wrappers] = process.argv.slice(2);
/** @type {(() => void)[]} */
const tasks = [];
/** @type {number[]} */
const calls = [];
class MessageChannel {
  constructor() {
    /** @type {{ close(): void, onmessage?: () => void }} */
    this.port1 = { close() {} };
    this.port2 = {
      close() {},
      postMessage: () => {
        tasks.push(() => /** @type {() => void} */ (this.port1.onmessage)());
      },
    };
  }
}
/** @type {Stand[]} */
const nodes = Array.from({ length: 35 }, (_, index) => ({
  index,
  dataset: {},
  querySelectorAll: () => [],
}));
/** @type {((value?: unknown) => void) | undefined} */
let finishLast;
Object.assign(globalThis, {
  MessageChannel,
  document: { documentElement: { dataset: {} } },
  kpressMathText: {
    /**
     * @param {string} _source
     * @param {Stand} target
     */
    render(_source, target) {
      calls.push(target.index);
      if (target === nodes.at(-1)) {
        return new Promise((resolve) => {
          finishLast = resolve;
        });
      }
      return Promise.resolve();
    },
  },
});
const flush = async () => {
  for (let i = 0; i < 8; i++) {
    await Promise.resolve();
  }
};

probe("devtools/probes/render_explainer/host_math_init.js")(wrappers);
/**
 * @type {{ render(el: Stand, source: string): Promise<boolean>, reserve(): () => void,
 *   batch(jobs: ReadonlyArray<() => unknown>): Promise<void>, submitted(): Promise<void>,
 *   settled(): Promise<void> }}
 */
const squaresMath = Reflect.get(globalThis, "squaresMath");

const finishBootstrap = squaresMath.reserve();
let complete = false;
const settled = squaresMath.settled().then(() => {
  complete = true;
});
await flush();
assert.equal(complete, false, "later boot scripts have not submitted their work");
const batch = squaresMath.batch(nodes.map((el) => () => squaresMath.render(el, "x")));
let submitted = false;
const submission = squaresMath.submitted().then(() => {
  submitted = true;
});
assert.equal(calls.length, 0, "queued work is registered before its first job");
await flush();
assert.equal(calls.length, 16, "one browser task has a bounded formula count");
assert.equal(
  nodes[0]?.dataset.squaresMathReady,
  "true",
  "an early formula can finish while later formulas are still queued",
);
finishBootstrap();
await flush();
assert.equal(complete, false, "the queue survives release of the boot reservation");
assert.equal(submitted, false, "the fallback-font probe must not alter queued work");
assert.equal(tasks.length, 1);
/** @type {() => void} */ (tasks.shift())();
await flush();
assert.equal(calls.length, 32);
assert.equal(complete, false);
/** @type {() => void} */ (tasks.shift())();
await flush();
assert.equal(calls.length, nodes.length);
await submission;
assert.equal(submitted, true, "font inspections finish while responses remain held");
assert.equal(complete, false, "the last issued formula still needs its font");
/** @type {(value?: unknown) => void} */ (finishLast)();
await batch;
await settled;
assert.equal(complete, true);
assert.deepEqual(
  calls,
  nodes.map((el) => el.index),
);
await assert.rejects(
  squaresMath.batch([
    () => {
      throw new Error("bad job");
    },
  ]),
);
await squaresMath.settled();
process.stdout.write("complete");
