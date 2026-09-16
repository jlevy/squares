// The shell's static math producer, `typeset` in `explainer-shell.html`: formulas go to the
// shared renderer by semantic priority (active panels, then the visible paper, then hidden
// copies), a failed native formula keeps its semantic fallback, and completion waits for the
// later certificate boots. Evaluated from the template itself, so the test reads the script
// the page ships. Prints `complete`.
//
// Usage: node static-math-priority.mjs <explainer-shell.html>
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { runInThisContext } from "node:vm";

/**
 * @typedef {{ name: string, dataset: Record<string, string>, textContent?: string,
 *   classList: { contains(value: string): boolean }, querySelector: () => unknown,
 *   closest(selector: string): object | null }} Stand
 */

const [template] = /** @type {[string]} */ (process.argv.slice(2));
const source = readFileSync(template, "utf8");
const start = source.indexOf("  const render = squaresMath.render;\n  async function typeset() {");
assert.notEqual(start, -1, "the shell has no static math producer");
const end = source.indexOf("  /* One copy of each figure", start);
assert.notEqual(end, -1, "the static math producer has no end");

/** @type {(() => Promise<unknown>)[]} */
const jobs = [];
/** @type {{ source: string, display: boolean }[]} */
const calls = [];
/** @type {string[]} */
const completed = [];
/**
 * @param {string} name
 * @param {{ hidden?: boolean, panel?: boolean, native?: boolean, display?: boolean }} [shape]
 * @returns {Stand}
 */
const makeNode = (
  name,
  { hidden = false, panel = false, native = false, display = false } = {},
) => {
  /** @type {{ dataset: Record<string, string>, textContent: string }} */
  const box = { dataset: { kpressMathSource: name }, textContent: "prepared markup" };
  /** @type {Stand} */
  const el = {
    name,
    dataset: native
      ? { kpressMath: display ? "display" : "inline", kpressMathRendered: "true" }
      : box.dataset,
    classList: {
      contains: (value) => value === (native ? "kpress-math" : display ? "tex-d" : "tex"),
    },
    querySelector: () => box,
    closest: (selector) =>
      selector === ".cert-figure[hidden]"
        ? hidden
          ? {}
          : null
        : selector === ".panel"
          ? panel
            ? {}
            : null
          : null,
  };
  if (!native) {
    el.textContent = box.textContent;
  }
  return el;
};
const nodes = [
  makeNode("hidden panel", { hidden: true, panel: true }),
  makeNode("body", { native: true }),
  makeNode("panel first", { panel: true }),
  makeNode("display", { display: true }),
  makeNode("failed native", { native: true, display: true }),
  makeNode("panel second", { panel: true }),
  makeNode("hidden body", { hidden: true }),
];
const missing = makeNode("missing native box", { native: true });
missing.querySelector = () => null;
const alreadyDone = makeNode("already done");
alreadyDone.dataset.done = "1";
nodes.push(missing, alreadyDone);
/** @type {((value?: unknown) => void) | undefined} */
let finishBatch;
/** @type {((value?: unknown) => void) | undefined} */
let finishBootstrap;
const squaresMath = {
  /**
   * @param {Stand} _el
   * @param {string} source
   * @param {boolean} display
   */
  render(_el, source, display) {
    calls.push({ source, display });
    return Promise.resolve(source !== "failed native");
  },
  /** @param {(() => Promise<unknown>)[]} queued */
  batch(queued) {
    jobs.push(...queued);
    return new Promise((resolve) => {
      finishBatch = resolve;
    });
  },
  settled() {
    return new Promise((resolve) => {
      finishBootstrap = resolve;
    });
  },
};
const flush = async () => {
  for (let i = 0; i < 4; i++) {
    await Promise.resolve();
  }
};
Object.assign(globalThis, {
  document: {
    /** @param {string} selector */
    querySelectorAll(selector) {
      assert.equal(selector, ".tex, .tex-d, .kpress-math");
      return nodes;
    },
    documentElement: {
      classList: {
        /** @param {string} value */
        add: (value) => completed.push(value),
      },
    },
  },
  window: {
    kpressInitTooltips() {
      completed.push("tooltips");
    },
    kpressInitCodeCopy() {
      completed.push("copy");
    },
  },
  kpressMathText: {
    complete() {
      completed.push("fonts");
    },
  },
  squaresMath,
});

runInThisContext(source.slice(start, end), { filename: template });
/** @type {() => Promise<void>} */
const typeset = Reflect.get(globalThis, "typeset");

const done = typeset();
assert.equal(calls.length, 0, "collecting math does not synchronously render it");
assert.ok(
  nodes.every((el) => el.dataset.squaresMathQueued === "true"),
  "unsubmitted wrappers remain hidden if the root watchdog expires",
);
await Promise.all(jobs.map((job) => job()));
assert.deepEqual(
  calls.map((call) => call.source),
  [
    "panel first",
    "panel second",
    "body",
    "display",
    "failed native",
    "hidden panel",
    "hidden body",
  ],
);
assert.equal(calls.find((call) => call.source === "display")?.display, true);
assert.equal(calls.find((call) => call.source === "failed native")?.display, true);
assert.equal(nodes[1]?.dataset.kpressMathRendered, "true");
assert.equal(
  nodes[4]?.dataset.kpressMathRendered,
  undefined,
  "a failed native formula keeps its semantic fallback",
);
assert.ok(
  nodes.every((el) => !el.dataset.squaresMathQueued),
  "successful and failed renders release their queued wrappers",
);
/** @type {(value?: unknown) => void} */ (finishBatch)();
await flush();
assert.deepEqual(completed, [], "the later certificate boots have not settled");
/** @type {(value?: unknown) => void} */ (finishBootstrap)();
await done;
assert.deepEqual(completed, ["fonts", "math-ready", "tooltips", "copy"]);
Object.assign(squaresMath, { batch: () => Promise.reject(new Error("submission failed")) });
await assert.rejects(typeset(), /submission failed/);
assert.ok(
  nodes.every((el) => !el.dataset.squaresMathQueued),
  "a failed producer cannot leave later wrappers hidden forever",
);
process.stdout.write("complete");
