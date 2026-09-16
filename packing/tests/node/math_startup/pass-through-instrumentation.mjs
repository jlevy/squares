// `check_math_startup/startup.js`: the instrument's wrappers keep the native promises and
// return values of every call they observe (both font-loading APIs, the math runtime's
// `ready`, `render` and `hydrate`, and KaTeX's `render`), count what they hook, and record
// each call's outcome once it settles.
import assert from "node:assert/strict";
import { probe } from "../probe.mjs";

/** @type {(value?: unknown) => void} */
let resolveFace = () => {};
/** @type {(value?: unknown) => void} */
let resolveSet = () => {};
/** @type {(value?: unknown) => void} */
let resolveReady = () => {};
/** @type {(value?: unknown) => void} */
let resolveRender = () => {};
const facePromise = new Promise((resolve) => {
  resolveFace = resolve;
});
const setPromise = new Promise((resolve) => {
  resolveSet = resolve;
});
const readyPromise = new Promise((resolve) => {
  resolveReady = resolve;
});
const renderPromise = new Promise((resolve) => {
  resolveRender = resolve;
});
Object.assign(globalThis, {
  FontFace: class {
    family = "probe";
    style = "normal";
    weight = "400";
    load() {
      assert.equal(this.family, "probe");
      return facePromise;
    }
  },
  document: {
    fonts: new (class {
      /** @param {string} value */
      load(value) {
        assert.equal(value, "16px probe");
        return setPromise;
      }
      addEventListener() {}
    })(),
    addEventListener() {},
  },
  addEventListener: () => {},
  requestAnimationFrame: () => {},
  MutationObserver: class {
    observe() {}
  },
});
Object.assign(globalThis, { window: globalThis });
assert.equal(Reflect.get(globalThis, "FontFaceSet"), undefined);

probe("devtools/probes/math/library.js")({ install: true });
probe("devtools/probes/check_math_startup/startup.js")({ mode: "full" });

const katexResult = Symbol("katex result");
Object.assign(globalThis, {
  katex: {
    /**
     * @param {string} source
     * @param {{ id: string }} target
     */
    render(source, target) {
      assert.equal(source, "x");
      assert.equal(target.id, "math");
      return katexResult;
    },
  },
  kpressMathText: {
    ready() {
      return readyPromise;
    },
    render() {
      return renderPromise;
    },
    hydrate() {
      return renderPromise;
    },
  },
});

/** @type {new () => { load(): unknown }} */
const FontFace = Reflect.get(globalThis, "FontFace");
/** @type {{ fonts: { load(value: string): unknown } }} */
const document = Reflect.get(globalThis, "document");
/** @type {{ ready(): unknown, render(source: string, target: object): unknown, hydrate(source: string, target: object): unknown }} */
const kpressMathText = Reflect.get(globalThis, "kpressMathText");
/** @type {{ render(source: string, target: object): unknown }} */
const katex = Reflect.get(globalThis, "katex");
/**
 * @typedef {{ outcome?: string, start_ms: number, end_ms?: number, duration_ms?: number }} Call
 * @type {{
 *   counters: Record<string, number>,
 *   katex: Call[], fonts: Call[], ready: Call[], renders: Call[], hydrates: Call[],
 * }}
 */
const state = Reflect.get(globalThis, "__mathStartup");

const target = { id: "math" };
assert.equal(new FontFace().load(), facePromise);
assert.equal(document.fonts.load("16px probe"), setPromise);
assert.equal(kpressMathText.ready(), readyPromise);
assert.equal(kpressMathText.render("x", target), renderPromise);
assert.equal(kpressMathText.hydrate("x", target), renderPromise);
assert.equal(katex.render("x", target), katexResult);
assert.equal(state.counters.font_hooks, 2);
assert.equal(state.counters.runtime_hooks, 2);
assert.equal(state.counters.hydrate_hooks, 1);
assert.equal(state.counters.hydrate_calls, 1);
assert.equal(state.counters.katex_calls, 1);
assert.ok(/** @type {number} */ (state.katex[0]?.duration_ms) >= 0);
assert.equal(state.fonts[0]?.outcome, "pending");
resolveFace();
resolveSet();
resolveReady();
resolveRender();
await Promise.resolve().then(() => {
  assert.ok(state.fonts.every((record) => record.outcome === "resolved"));
  assert.equal(state.ready[0]?.outcome, "resolved");
  assert.equal(state.renders[0]?.outcome, "resolved");
  assert.equal(state.hydrates[0]?.outcome, "resolved");
  assert.ok(
    state.fonts.every((record) => /** @type {number} */ (record.end_ms) >= record.start_ms),
  );
});
