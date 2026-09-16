// `math/library.js`'s `requiredFonts`: each CSS family in a glyph run is observed on its own,
// hidden staging included, so a loaded first family cannot hide a pending later face.
import assert from "node:assert/strict";
import { probe } from "../probe.mjs";

/** @param {string} family */
const parent = (family) => ({
  style: { fontStyle: "normal", fontWeight: "400", fontSize: "16px", fontFamily: family },
  checkVisibility: () => false,
});
const composite = '"KPress Math, Text Sans",KaTeX_Main,serif';
const nodes = [
  { textContent: "x1", parentElement: parent(composite) },
  { textContent: "1≈", parentElement: parent(composite) },
  { textContent: "∑", parentElement: parent("KaTeX_Size2") },
];
const html = {};
Object.assign(globalThis, {
  NodeFilter: { SHOW_TEXT: 4 },
  /** @param {{ style: object }} node */
  getComputedStyle: (node) => node.style,
  document: {
    /** @param {object} node */
    createTreeWalker(node) {
      assert.equal(node, html);
      let index = -1;
      return {
        nextNode() {
          return ++index < nodes.length;
        },
        get currentNode() {
          return nodes[index];
        },
      };
    },
  },
});
const math = {
  /** @param {string} selector */
  querySelector: (selector) => {
    assert.equal(selector, ".katex-html");
    return html;
  },
};
/** @type {{ spec: string, text: string }[]} */
const checked = [];
/**
 * @param {string} spec
 * @param {string} text
 */
const observe = (spec, text) => {
  checked.push({ spec, text });
  return { ready: !spec.includes("KaTeX_Main") };
};

/** @type {{ ready: boolean }[]} */
const result = probe("devtools/probes/math/library.js")().requiredFonts(math, observe);
assert.deepEqual(checked, [
  { spec: 'normal 400 16px "KPress Math, Text Sans"', text: "x1≈" },
  { spec: "normal 400 16px KaTeX_Main", text: "x1≈" },
  { spec: "normal 400 16px serif", text: "x1≈" },
  { spec: "normal 400 16px KaTeX_Size2", text: "∑" },
]);
assert.equal(result[0]?.ready, true);
assert.equal(
  result[1]?.ready,
  false,
  "a loaded first family cannot hide a pending later relation face",
);
assert.equal(result[2]?.ready, true);
assert.equal(result[3]?.ready, true);
