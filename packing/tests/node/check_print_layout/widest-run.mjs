// `check_print_layout/layout_helpers.js`'s culprit scan, `widestRun` and the `inkRight` it
// calls, over enough of a DOM to walk: a rectangle, a parent, and the computed properties
// `inkRight` reads. `sig` is a stand-in that answers with the element's name, the shipped
// `sig` wanting a real `classList` and `children`; `round` and the scan are the shipped
// ones. Geometry goes in as rectangles retained from the browser. Prints the widest run, or
// `null`.
//
//   node widest-run.mjs mathml <style JSON>
//   node widest-run.mjs escaping <style JSON>
//
// `mathml` is the tau* equation's MathML chain and `--self-check`'s injected block, as the
// rendered explainer lays them out under `emulateMedia('print')` in a 576px column. KaTeX
// puts a MathML transcription of every formula in a `.katex-mathml` span that is 1px wide,
// and the boxes inside it keep their natural width: the `mrow` ends at 812.77px, 236.77px
// past a page that its ink never reaches. The style is that wrapper's; the explainer's is
// absolute with `overflow: hidden` and `clip: rect(1px, 1px, 1px, 1px)`.
//
// `escaping` is synthesized rather than retained: this page has no such box. An absolutely
// positioned element is laid out in its containing block, so a clipping ancestor below that
// block does not cut it, and it really does widen the document. The style is the clipping
// ancestor's.
import { probe } from "../probe.mjs";

const [scene, styleJSON] = process.argv.slice(2);
/** @type {Record<string, string>} */
const style = JSON.parse(styleJSON ?? "");

/**
 * @typedef {{ name: string, textContent: string, closest: () => null, parentElement: Stand | null, style: Record<string, string>, getBoundingClientRect: () => { left: number, right: number, width: number } }} Stand
 */
const plain = { position: "static", overflowX: "visible", clip: "auto", clipPath: "none" };
/**
 * @param {string} name
 * @param {number} left
 * @param {number} right
 * @param {Record<string, string>} [over]
 * @returns {Stand}
 */
const el = (name, left, right, over) => ({
  name,
  textContent: name,
  closest: () => null,
  parentElement: null,
  style: { ...plain, ...over },
  getBoundingClientRect: () => ({ left, right, width: right - left }),
});
/** @param {Stand[]} nodes */
const stack = (...nodes) => {
  for (let i = 0; i < nodes.length - 1; i++) {
    /** @type {Stand} */ (nodes[i]).parentElement = /** @type {Stand} */ (nodes[i + 1]);
  }
  return nodes[0];
};
const root = { clientWidth: 576 };

/** @type {Stand[]} */
let candidates;
if (scene === "mathml") {
  const html = el("html.math-ready", 0, 576);
  const body = el("body.kpress-frame", 0, 576);
  const main = el("main.kpress-viewport", 0, 576, { position: "relative" });
  const column = el("div.kpress", 0, 576);
  const render = el("div.kpress-math-render", 0, 576);
  const display = el("span.katex-display", 0, 576);
  const katex = el("span.katex", 0, 576, { position: "relative" });
  const mathml = el("span.katex-mathml", 288, 289, style);
  const math = el("math", 288, 289);
  const semantics = el("semantics", 288, 289);
  const mrow = el("mrow", 288, 812.765625);
  const injected = el("div.print-layout-self-check", 0, 618);
  stack(mrow, semantics, math, mathml, katex, display, render, column, main, body, html);
  stack(injected, column);
  candidates = [mrow, semantics, math, mathml, injected];
} else if (scene === "escaping") {
  const html = el("html", 0, 576);
  const body = el("body", 0, 576);
  const clipper = el("div.clipper", 0, 576, style);
  const escapee = el("div.escapee", 0, 618, { position: "absolute" });
  stack(escapee, clipper, body, html);
  candidates = [escapee];
} else {
  throw new Error(`no scene ${scene}`);
}
Object.assign(globalThis, {
  document: { querySelectorAll: () => candidates },
  /** @param {Stand} node */
  getComputedStyle: (node) => node.style,
});

const { round } = probe("devtools/probes/check_print_layout/naming.js")();
/** @type {{ widestRun: (root: object) => object | null }} */
const { widestRun } = probe("devtools/probes/check_print_layout/layout_helpers.js")({
  /** @param {Stand} node */
  sig: (node) => node.name,
  round,
});
process.stdout.write(JSON.stringify(widestRun(root) ?? null));
