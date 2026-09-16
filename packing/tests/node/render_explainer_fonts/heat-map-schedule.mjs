// The shell's `scheduleHeat` in `explainer-shell.html`: expensive canvas work starts after the
// required math settles and a paint occurs, only one heat-map task may be pending, a
// certificate hidden since scheduling is not drawn, and a completed heat map is reused.
// Evaluated from the template itself, so the test reads the script the page ships.
//
// Usage: node heat-map-schedule.mjs <explainer-shell.html>
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { runInThisContext } from "node:vm";

const [template] = /** @type {[string]} */ (process.argv.slice(2));
const source = readFileSync(template, "utf8");
const start = source.indexOf("function scheduleHeat() {");
assert.notEqual(start, -1, "the shell has no heat-map scheduler");
const end = source.indexOf("\nfunction toWorld(", start);
assert.notEqual(end, -1, "the heat-map scheduler has no end");

/** @type {((value?: unknown) => void) | undefined} */
let finish;
let hidden = false;
let draws = 0,
  builds = 0,
  settlements = 0;
/** @type {(() => void)[]} */
const frames = [];
/** @type {(() => void)[]} */
const tasks = [];
const pending = new Promise((resolve) => {
  finish = resolve;
});
// The scheduler reads and writes these three as the page script's own variables.
Object.assign(globalThis, {
  heatQueued: false,
  heat: null,
  showHeat: true,
  squaresMath: {
    settled: () => {
      settlements++;
      return pending;
    },
  },
  pv: { closest: () => ({ hidden }) },
  /** @param {() => void} callback */
  requestAnimationFrame: (callback) => frames.push(callback),
  /** @param {() => void} callback */
  setTimeout: (callback) => tasks.push(callback),
  buildHeat: () => {
    Object.assign(globalThis, { heat: {} });
    builds++;
  },
  drawProver: () => {
    draws++;
  },
});

runInThisContext(source.slice(start, end), { filename: template });
/** @type {() => void} */
const scheduleHeat = Reflect.get(globalThis, "scheduleHeat");
/** @param {(() => void)[]} queue */
const next = (queue) => /** @type {() => void} */ (queue.shift())();

scheduleHeat();
scheduleHeat();
assert.equal(settlements, 1, "only one heat-map task may be pending");
assert.equal(frames.length, 0, "pending math has not yet reached a paint");
/** @type {(value?: unknown) => void} */ (finish)();
await Promise.resolve();
assert.equal(frames.length, 1);
assert.equal(builds, 0);
next(frames);
assert.equal(builds, 0, "the animation-frame callback still lets a paint through");
hidden = true;
next(tasks);
assert.equal(builds, 0, "a certificate hidden since scheduling is not drawn");
hidden = false;
scheduleHeat();
await Promise.resolve();
next(frames);
next(tasks);
assert.equal(builds, 1);
assert.equal(draws, 1);
scheduleHeat();
assert.equal(frames.length, 0, "a completed heat map is reused");
