// `check_print_layout/rotation_target.js` over one stand-in handle. With `true` it has every
// known touch defect: 43px wide, an unnamed `div`, covered where a finger lands, allowing
// the browser to cancel its drag, beside a canvas that blocks vertical scrolling. With
// `false` it has none. Prints the findings.
//
//   node rotation-target.mjs <true|false>
import { probe } from "../probe.mjs";

const broken = JSON.parse(process.argv[2] ?? "");

const handle = {
  getBoundingClientRect: () => ({ x: 10, y: 20, width: broken ? 43 : 44, height: 44 }),
  tagName: broken ? "DIV" : "BUTTON",
  getAttribute: () => (broken ? "" : "Rotate the unit square"),
  contains: () => !broken,
  touchAction: broken ? "pan-y" : "none",
  closest: () => ({ querySelector: () => ({ touchAction: broken ? "none" : "pan-y" }) }),
};
Object.assign(globalThis, {
  document: { elementFromPoint: () => handle },
  /** @param {object} el */
  getComputedStyle: (el) => el,
});

/** @type {(handle: object) => string[]} */
const rotationTarget = probe("devtools/probes/check_print_layout/rotation_target.js");
process.stdout.write(JSON.stringify(rotationTarget(handle)));
