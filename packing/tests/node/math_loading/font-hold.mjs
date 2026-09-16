// `check_math_loading/hold_fonts.js`: holds both font-loading APIs without a global
// `FontFaceSet` constructor, lets empty matches through, and gives the observer a native load.
import assert from "node:assert/strict";
import { probe } from "../probe.mjs";

/** @type {unknown[][]} */
const calls = [];
Object.assign(globalThis, {
  FontFace: class {
    /** @param {unknown[]} args */
    load(...args) {
      calls.push(["face", ...args]);
      return Promise.resolve(this);
    }
  },
});
const document = {
  fonts: new (class {
    /** @param {string[]} args */
    load(...args) {
      calls.push(["set", ...args]);
      return Promise.resolve(String(args[0]).includes("excluded") ? [] : ["matched face"]);
    }
    /**
     * @param {string} spec
     * @param {string} text
     */
    check(spec, text) {
      return spec === "16px test" && text === "x";
    }
  })(),
};
Object.assign(globalThis, { document });
assert.equal("FontFaceSet" in globalThis, false);

probe("devtools/probes/check_math_loading/hold_fonts.js")();
/** @type {{ heldLoads: number, release(): void, nativeLoad(spec: string): Promise<unknown> }} */
const control = Reflect.get(globalThis, "__mathLoadControl");
const FontFace = Reflect.get(globalThis, "FontFace");

let matchedDone = false,
  emptyDone = false;
const requests = [
  new FontFace().load("face argument"),
  document.fonts.load("12px test").then(() => {
    matchedDone = true;
  }),
  document.fonts.load("12px excluded").then(() => {
    emptyDone = true;
  }),
];
assert.equal(document.fonts.check("16px test", "x"), true);
assert.deepEqual(
  await control.nativeLoad("16px test"),
  ["matched face"],
  "the independent observer bypasses the test gate",
);
await Promise.resolve();
assert.equal(control.heldLoads, 2);
assert.equal(matchedDone, false);
assert.equal(emptyDone, true, "excluded Unicode/system families must not be held");
assert.equal(
  calls.some(([kind]) => kind === "face"),
  false,
);
control.release();
await Promise.all(requests);
assert.equal(matchedDone, true);
assert.equal(document.fonts.check("16px missing", "x"), false);
assert.deepEqual(calls, [
  ["set", "12px test"],
  ["set", "12px excluded"],
  ["set", "16px test"],
  ["face", "face argument"],
]);
