// `math/library.js`'s `fontLoadObserver`: readiness comes from the observed load promises and
// the faces they resolve to, never from `document.fonts.check`, which WebKit can answer wrongly.
import assert from "node:assert/strict";
import { probe } from "../probe.mjs";

/** @type {{ spec: string, text: string, resolve: (faces: object[]) => void, reject: (error: Error) => void }[]} */
const requests = [];
/**
 * @param {string} spec
 * @param {string} text
 */
const load = (spec, text) =>
  new Promise((resolve, reject) => {
    requests.push({ spec, text, resolve, reject });
  });
const document = {
  fonts: {
    /**
     * @param {string} _spec
     * @param {string} _text
     */
    check: (_spec, _text) => true,
  },
};
const face = {
  family: "KaTeX_Main",
  style: "normal",
  weight: "400",
  unicodeRange: "U+2265",
  status: "error",
};

/** @type {(spec: string, text: string) => { ready: boolean, outcome: string, faces: { status: string }[], error?: string }} */
const observe = probe("devtools/probes/math/library.js")().fontLoadObserver(load);
/** @param {number} index */
const request = (index) => /** @type {(typeof requests)[number]} */ (requests[index]);

const spec = 'normal 400 16px "KaTeX_Main"';
assert.equal(observe(spec, "≥").ready, false);
assert.equal(observe(spec, "≥").outcome, "pending");
assert.equal(requests.length, 1, "identical descriptions share an observed promise");
assert.equal(
  document.fonts.check(spec, "≥"),
  true,
  "the WebKit false-positive must not make the oracle ready",
);
request(0).resolve([face]);
await Promise.resolve();
assert.equal(
  observe(spec, "≥").ready,
  false,
  "a resolved promise with an error face is still unavailable",
);
assert.equal(observe(spec, "≥").faces[0]?.status, "error");
face.status = "loaded";
assert.equal(observe(spec, "≥").ready, true);

assert.equal(observe("normal 400 16px serif", "≥").ready, false);
request(1).resolve([]);
await Promise.resolve();
assert.equal(
  observe("normal 400 16px serif", "≥").ready,
  true,
  "a system family or excluded Unicode range needs no declared face",
);

observe(spec, "≈");
request(2).reject(new Error("required face failed"));
await Promise.resolve();
assert.equal(observe(spec, "≈").ready, false);
assert.equal(observe(spec, "≈").outcome, "rejected");
assert.match(String(observe(spec, "≈").error), /required face failed/);
observe('italic 400 16px "KaTeX_Main"', "≥");
observe('normal 700 16px "KaTeX_Main"', "≥");
observe('normal 400 18px "KaTeX_Main"', "≥");
observe('normal 400 16px "KaTeX_AMS"', "≥");
assert.equal(requests.length, 7, "style, weight, size, family, and text key the cache");
