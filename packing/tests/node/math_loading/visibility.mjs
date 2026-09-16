// `math/library.js`'s `exposed`: visibility requires readable geometry after ancestor overflow,
// legacy clip rectangles and inset clip paths, and follows content a reader can scroll to.
import assert from "node:assert/strict";
import { probe } from "../probe.mjs";

/**
 * @typedef {{ left: number, top: number, right: number, bottom: number, width: number, height: number }} Box
 * @typedef {{ style: Record<string, string>, parentElement: Stand | null, scrollHeight?: number, clientHeight?: number, checkVisibility(options: { opacityProperty: boolean, visibilityProperty: boolean }): boolean, getBoundingClientRect(): Box }} Stand
 */

Object.assign(globalThis, {
  /** @param {Stand} node */
  getComputedStyle: (node) => node.style,
});
/**
 * @param {Record<string, string>} [style]
 * @param {number} [width]
 * @param {number} [height]
 * @param {Stand | null} [parent]
 * @returns {Stand}
 */
const element = (style = {}, width = 100, height = 20, parent = null) => ({
  style,
  parentElement: parent,
  checkVisibility(options) {
    assert.equal(options.opacityProperty, true);
    assert.equal(options.visibilityProperty, true);
    return true;
  },
  getBoundingClientRect: () => ({ left: 0, top: 0, right: width, bottom: height, width, height }),
});

/** @type {(node: Stand) => boolean} */
const exposed = probe("devtools/probes/math/library.js")().exposed;
assert.equal(exposed(element()), true);
assert.equal(exposed(element({}, 1, 1)), false, "clipped accessibility text is not visible");
assert.equal(exposed(element({ clipPath: "inset(50%)" })), false);
assert.equal(exposed(element({ clipPath: "inset(0px)" })), true);
assert.equal(exposed(element({ clip: "rect(0px, 0px, 0px, 0px)" })), false);
assert.equal(exposed(element({}, 100, 20, element({ overflowX: "hidden" }, 1))), false);
assert.equal(exposed(element({}, 100, 20, element({ clipPath: "inset(50%)" }))), false);
const frame = element({ overflowY: "hidden" }, 100, 720);
const scroll = element({ overflowY: "auto" }, 100, 720, frame);
scroll.scrollHeight = 10000;
scroll.clientHeight = 720;
const belowFold = element({}, 100, 20, scroll);
belowFold.getBoundingClientRect = () => ({
  left: 0,
  top: 1000,
  right: 100,
  bottom: 1020,
  width: 100,
  height: 20,
});
assert.equal(exposed(belowFold), true, "scrolling can expose readable fallback");
