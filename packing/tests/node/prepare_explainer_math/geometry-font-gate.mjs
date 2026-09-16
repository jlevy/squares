// `prepare_explainer_math/geometry_font_trace.js`: the geometry probe's own setup cannot
// consume KPress's timeout budget. The gate pauses the root watchdog, holds every math call
// until the before snapshot is marked complete, then passes calls, return values, synchronous
// throws and rejections through unchanged, tracing the rejections.
import assert from "node:assert/strict";
import { probe } from "../probe.mjs";

probe("devtools/probes/prepare_explainer_math/geometry_font_trace.js")();

/** @type {[string, string, number][]} */
const starts = [];
const postReleasePromise = Promise.resolve("post-release");
const synchronousError = new Error("synchronous failure");
const rejection = new Error("post-release rejection");
/** @type {Promise<never> | undefined} */
let rejectedPromise;
/** @type {{ documentElement: { dataset: Record<string, string> } }} */
const document = { documentElement: { dataset: { kpressMathPending: "true" } } };
Object.assign(globalThis, {
  kpressMathText: {
    /** @param {string} source */
    render(source) {
      starts.push(["render", source, performance.now()]);
      if (source === "post-release") {
        return postReleasePromise;
      }
      if (source === "throw") {
        throw synchronousError;
      }
      if (source === "reject") {
        rejectedPromise = Promise.reject(rejection);
        return rejectedPromise;
      }
      return Promise.resolve("rendered");
    },
    /** @param {string} source */
    hydrate(source) {
      starts.push(["hydrate", source, performance.now()]);
      return Promise.resolve("hydrated");
    },
  },
});

/** @type {{ render(source: string): unknown, hydrate(source: string): unknown }} */
const kpressMathText = Reflect.get(globalThis, "kpressMathText");
/**
 * @type {{
 *   root_watchdog_paused: boolean,
 *   first_math_request_ms: number | null,
 *   queued_calls: number,
 *   rejections: { source: string }[],
 * }}
 */
const trace = Reflect.get(globalThis, "__squaresGeometryFontTrace");
/** @type {() => void} */
const markBeforeSnapshotComplete = Reflect.get(
  globalThis,
  "__squaresMarkGeometryBeforeSnapshotComplete",
);
/** @type {() => void} */
const releaseGate = Reflect.get(globalThis, "__squaresReleaseGeometryFontGate");
// Read through a call: an assertion that it is null must not narrow later reads.
const firstRequest = () => trace.first_math_request_ms;

Object.assign(globalThis, {
  kpressMathPendingTimer: setTimeout(() => {
    delete document.documentElement.dataset.kpressMathPending;
  }, 0),
});
await new Promise((resolve) => setTimeout(resolve, 10));
assert.equal(document.documentElement.dataset.kpressMathPending, "true");
assert.equal(trace.root_watchdog_paused, true);
const rendered = kpressMathText.render("x");
const hydrated = kpressMathText.hydrate("y");
await Promise.resolve();
const beforeSnapshotCompleted = performance.now();
assert.deepEqual([...starts], []);
assert.equal(firstRequest(), null);
assert.equal(trace.queued_calls, 2);
assert.throws(() => releaseGate(), /released before the before snapshot/);
assert.deepEqual([...starts], []);
markBeforeSnapshotComplete();
releaseGate();
assert.deepEqual(
  starts.map((call) => call.slice(0, 2)),
  [
    ["render", "x"],
    ["hydrate", "y"],
  ],
);
assert.ok(starts.every((call) => call[2] >= beforeSnapshotCompleted));
assert.ok(/** @type {number} */ (firstRequest()) >= beforeSnapshotCompleted);
assert.deepEqual(await Promise.all([rendered, hydrated]), ["rendered", "hydrated"]);
assert.strictEqual(kpressMathText.render("post-release"), postReleasePromise);
assert.throws(
  () => kpressMathText.render("throw"),
  (error) => error === synchronousError,
);
const observedRejection = kpressMathText.render("reject");
assert.strictEqual(observedRejection, rejectedPromise);
await assert.rejects(/** @type {Promise<unknown>} */ (observedRejection), /post-release rejection/);
assert.deepEqual(
  trace.rejections.map((entry) => entry.source),
  ["throw", "reject"],
);
process.stdout.write("complete");
