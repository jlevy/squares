// `check_print_layout/prover_layout.js`, the browser's own predicate, over contrasting
// geometry and font measurements for one Figure 5. With `true` every stand-in carries a
// known defect: the earlier side panel, a wrapping and overflowing direction item, a
// reduced-size fraction, and a hidden status that still has a box. With `false` none does.
// Prints the findings.
//
//   node prover-layout.mjs <true|false>
import { probe } from "../probe.mjs";

const broken = JSON.parse(process.argv[2] ?? "");

const panel = {
  getBoundingClientRect: () => ({ top: broken ? 20 : 300, left: 0, right: 400 }),
};
const stage = { getBoundingClientRect: () => ({ bottom: 300 }) };
const digit = { children: [], textContent: "4001", fontSize: broken ? "14px" : "20px" };
const mass = {
  fontSize: "20px",
  closest: () => null,
  querySelectorAll: () => [digit],
  querySelector: () => ({}),
};
/** @type {Record<string, unknown>} */
const item = {
  whiteSpace: broken ? "normal" : "nowrap",
  closest: () => null,
  getBoundingClientRect: () => ({ left: broken ? -20 : 20, right: broken ? 450 : 380 }),
  /** @param {string} selector */
  querySelector: (selector) => (selector === ".katex" ? mass : item),
  /** @param {string} selector */
  querySelectorAll: (selector) => [selector === ".katex" ? mass : item],
};
const hidden = { getClientRects: () => (broken ? [{}] : []) };
/** @type {Record<string, unknown>} */
const selected = {
  ".panel": panel,
  ".stage": stage,
  ".math-item": item,
  ".mass-val .katex": mass,
};
/** @type {Record<string, unknown[]>} */
const all = { ".math-item": [item], ".mass-val .katex": [mass], "[hidden]": [hidden] };
const figure = {
  getClientRects: () => [{}],
  /** @param {string} selector */
  querySelector: (selector) => selected[selector],
  /** @param {string} selector */
  querySelectorAll: (selector) => all[selector],
};
Object.assign(globalThis, {
  document: { documentElement: { dataset: {} }, querySelectorAll: () => [figure] },
  /** @param {object} el */
  getComputedStyle: (el) => el,
});

const math = probe("devtools/probes/math/library.js")();
/** @type {(o: { math: object }) => string[]} */
const proverLayout = probe("devtools/probes/check_print_layout/prover_layout.js");
process.stdout.write(JSON.stringify(proverLayout({ math })));
