// `check_print_layout/layout_helpers.js`'s `firstLineBox` over the printed mass-condition
// bullet's Range rectangles: inline tops at -1, 0, 2 and 3px share one line, and the next
// line starts a full line height below it. Prints the line box.
import { probe } from "../probe.mjs";

const rects = [
  { top: 0, bottom: 22, height: 22, width: 100 },
  { top: 0, bottom: 22.390625, height: 22.390625, width: 20 },
  { top: -1, bottom: 19, height: 20, width: 10 },
  { top: 2, bottom: 22, height: 20, width: 10 },
  { top: 3, bottom: 21, height: 18, width: 10 },
  { top: 22.390625, bottom: 44.390625, height: 22, width: 100 },
];
Object.assign(globalThis, {
  document: {
    createRange: () => ({
      selectNodeContents() {},
      getClientRects: () => rects,
    }),
  },
});
const el = { querySelectorAll: () => [] };

/** @type {{ firstLineBox: (el: object) => object | null }} */
const { firstLineBox } = probe("devtools/probes/check_print_layout/layout_helpers.js")(
  probe("devtools/probes/check_print_layout/naming.js")(),
);
process.stdout.write(JSON.stringify(firstLineBox(el)));
