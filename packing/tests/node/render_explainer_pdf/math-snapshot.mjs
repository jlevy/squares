// `render_explainer_pdf/math_snapshot.js` and `prepared_text_intervention.js`: the snapshot
// tracks visible prepared text without hiding omissions, and the intervention refuses a
// truncated selection, leaves the control arm untouched, and replaces exactly the selected
// nodes in the treatment arm.
//
//   node math-snapshot.mjs [overflow]
//
// With `overflow`, the page carries more text nodes than the snapshot's token limit.
import assert from "node:assert/strict";
import { probe } from "../probe.mjs";

const overflow = process.argv[2] === "overflow";

// Stand-ins are loose on purpose: each carries only what the probes read.
/**
 * @typedef {{ children: Stand[], parentElement: Stand | null, [key: string]: any }} Stand
 * @typedef {{ data: string, parentElement: Stand, parentNode: Stand, boxes: object[], [key: string]: any }} TextStand
 */

const box = { x: 10, y: 20.21875, width: 24, height: 16 };
const style = {
  display: "inline",
  height: "20.08336px",
  fontFamily: "PT Serif",
  fontSize: "16px",
  lineHeight: "0px",
  verticalAlign: "baseline",
  fontWeight: "400",
  fontStyle: "normal",
  position: "static",
  textRendering: "auto",
  fontKerning: "auto",
};
/**
 * @param {Stand | null} parent
 * @param {boolean} [shown]
 * @returns {Stand}
 */
const element = (parent, shown = true) => {
  /** @type {Stand} */
  const result = {
    tagName: "SPAN",
    className: "mop",
    parentElement: parent,
    children: [],
    checkVisibility: () => shown,
    getBoundingClientRect: () => box,
  };
  parent?.children.push(result);
  return result;
};
const host = element(null),
  html = element(host),
  owner = element(html);
const hidden = element(html, false);
host.dataset = { kpressMathSource: "\\tan d \\le D" };
host.querySelector = () => html;
html.querySelectorAll = () => [owner];
/**
 * @param {string} value
 * @param {Stand} [parent]
 * @param {object[]} [boxes]
 * @returns {TextStand}
 */
const text = (value, parent = owner, boxes = [box]) => ({
  data: value,
  textContent: value,
  parentElement: parent,
  parentNode: parent,
  boxes,
});
const nodes = [text(" "), text("hidden", hidden), text("tan"), text("clipped", owner, [])];
/**
 * @param {TextStand} replacement
 * @param {TextStand} original
 */
owner.replaceChild = (replacement, original) => {
  const index = nodes.indexOf(original);
  assert.ok(index >= 0);
  replacement.parentNode = owner;
  replacement.parentElement = owner;
  nodes[index] = replacement;
};
const fonts = Object.assign(
  [
    {
      family: "PT Serif",
      style: "normal",
      weight: "400",
      stretch: "normal",
      status: "loaded",
      unicodeRange: "U+0-10FFFF",
    },
  ],
  { status: "loaded" },
);
Object.assign(globalThis, {
  getComputedStyle: () => style,
  NodeFilter: { SHOW_TEXT: 4 },
  document: {
    querySelectorAll: () => [{ querySelector: () => null }, host],
    fonts,
    documentElement: {
      get outerHTML() {
        return `<html>${nodes.map((node) => node.data).join("")}</html>`;
      },
    },
    createTreeWalker: () => {
      let next = 0;
      return { nextNode: () => nodes[next++] || null };
    },
    createTextNode: (/** @type {string} */ value) => text(value),
    createRange: () => ({
      /** @type {TextStand | null} */
      node: null,
      /** @param {TextStand} node */
      selectNodeContents(node) {
        this.node = node;
      },
      getClientRects() {
        return this.node?.boxes;
      },
    }),
  },
});
if (overflow) {
  nodes.push(...Array.from({ length: 10000 }, () => text("x".repeat(513))));
}

/**
 * @typedef {{ phase: string, font_status: string, fonts: { family: string }[], token_limit: number, truncated: boolean, formulas: { formula: number, source: string, boxes: { rect: { y: number }, vertical_align: string }[], bases: { line_height: string }[], struts: { height: string }[] }[], tokens: { text: string, text_truncated: boolean }[] }} Snapshot
 * @typedef {{ error?: string, snapshots: Snapshot[], intervention: { status: string, applied: boolean, selected_count: number, mutated_count: number, html_unchanged: boolean, selected: object[], mutated: object[], after_selected: object[] } }} Intervention
 */
/** @type {(phase: string, selected?: object[] | null) => Snapshot} */
const snapshotter = probe("devtools/probes/render_explainer_pdf/math_snapshot.js")();
/** @type {(o: { rebuild: boolean, snapshot: typeof snapshotter }) => Intervention} */
const intervention = probe("devtools/probes/render_explainer_pdf/prepared_text_intervention.js");
/** @param {boolean} rebuild */
const intervene = (rebuild) => intervention({ rebuild, snapshot: snapshotter });

const snapshot = snapshotter("before-pdf");
const formula = /** @type {Snapshot["formulas"][number]} */ (snapshot.formulas[0]);
assert.equal(snapshot.phase, "before-pdf");
assert.equal(snapshot.font_status, "loaded");
assert.equal(snapshot.fonts[0]?.family, "PT Serif");
assert.equal(formula.formula, 1);
assert.equal(formula.source, "\\tan d \\le D");
assert.equal(formula.boxes[0]?.rect.y, 20.21875);
assert.equal(formula.boxes[0]?.vertical_align, "baseline");
assert.equal(formula.bases[0]?.line_height, "0px");
assert.equal(formula.struts[0]?.height, "20.08336px");
assert.deepEqual(snapshot.tokens[0], {
  formula: 1,
  token: 2,
  path: "span:1/span:1",
  text: "tan",
  text_truncated: false,
  class_name: "mop",
  element_rect: box,
  text_rects: [box],
  font_family: "PT Serif",
  font_size: "16px",
  font_weight: "400",
  font_style: "normal",
  line_height: "0px",
  vertical_align: "baseline",
  position: "static",
  text_rendering: "auto",
  font_kerning: "auto",
});

if (overflow) {
  assert.equal(snapshot.truncated, true);
  assert.equal(snapshot.tokens.length, snapshot.token_limit);
  assert.equal(snapshot.tokens[1]?.text.length, 512);
  assert.equal(snapshot.tokens[1]?.text_truncated, true);
  const original = [...nodes];
  const refused = intervene(true);
  assert.match(String(refused.error), /truncated before replacement/);
  assert.equal(refused.intervention.status, "refused");
  assert.equal(refused.intervention.mutated_count, 0);
  assert.equal(refused.snapshots.length, 1);
  assert.deepEqual(nodes, original);
} else {
  assert.equal(snapshot.truncated, false);
  assert.equal(snapshot.tokens.length, 1);
  const original = [...nodes];
  const control = intervene(false);
  assert.equal(control.error, undefined);
  assert.equal(control.intervention.status, "control");
  assert.equal(control.intervention.applied, false);
  assert.equal(control.intervention.selected_count, 1);
  assert.equal(control.intervention.mutated_count, 0);
  assert.equal(control.intervention.html_unchanged, true);
  assert.deepEqual(control.intervention.selected, [
    { formula: 1, token: 2, path: "span:1/span:1", text: "tan" },
  ]);
  assert.deepEqual(nodes, original);
  assert.deepEqual(
    control.snapshots.map((s) => s.phase),
    ["before-intervention", "after-intervention"],
  );
  const treatment = intervene(true);
  assert.equal(treatment.error, undefined);
  assert.equal(treatment.intervention.status, "applied");
  assert.equal(treatment.intervention.applied, true);
  assert.equal(treatment.intervention.selected_count, 1);
  assert.equal(treatment.intervention.mutated_count, 1);
  assert.equal(treatment.intervention.html_unchanged, true);
  assert.deepEqual(treatment.intervention.mutated, control.intervention.selected);
  assert.deepEqual(treatment.intervention.after_selected, control.intervention.selected);
  assert.notEqual(nodes[2], original[2]);
  for (const index of [0, 1, 3]) {
    assert.equal(nodes[index], original[index]);
  }
  assert.equal(
    nodes.map((node) => node.data).join("|"),
    original.map((node) => node.data).join("|"),
  );
  assert.deepEqual(
    treatment.snapshots.map((s) => s.phase),
    ["before-intervention", "after-intervention"],
  );
  nodes.length = 0;
  const noTargets = intervene(true);
  assert.match(String(noTargets.error), /no visible prepared-text nodes selected/);
  assert.equal(noTargets.intervention.status, "no-targets");
  assert.equal(noTargets.intervention.applied, false);
  assert.equal(noTargets.intervention.mutated_count, 0);
}
