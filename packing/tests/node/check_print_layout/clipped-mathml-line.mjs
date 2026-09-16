// `check_print_layout/layout_helpers.js`'s `firstLineBox` over retained mass-condition
// geometry, where the semantic MathML's rectangles rise above the real line. Its computed
// `position` is the argument: `absolute` with its clip is the hidden annotation, whose
// rectangles are removed, and `static` is visible fallback, which contributes. Prints the
// line box.
//
//   node clipped-mathml-line.mjs <position>
import { probe } from "../probe.mjs";

const position = process.argv[2];
const semantic = {
  style: { position, clip: "rect(1px, 1px, 1px, 1px)", clipPath: "none" },
  rects: [
    { top: 1, bottom: 2, height: 1, width: 1, left: 600, right: 601 },
    { top: -3.6875, bottom: 18.3125, height: 22, width: 9, left: 600, right: 609 },
  ],
};
const el = {
  /** @param {string} selector */
  querySelectorAll: (selector) => (selector.startsWith("sup") ? [] : [semantic]),
  rects: [
    { top: 1, bottom: 25, height: 24, width: 600, left: 0, right: 600 },
    { top: 1, bottom: 26.1875, height: 25.1875, width: 12, left: 600, right: 612 },
    ...semantic.rects,
    { top: 4.015625, bottom: 25.609375, height: 21.59375, width: 9, left: 600, right: 609 },
  ],
};
Object.assign(globalThis, {
  /** @param {{ style: object }} node */
  getComputedStyle: (node) => node.style,
  document: {
    createRange: () => {
      /** @type {{ rects: object[] }} */
      let selected;
      return {
        /** @param {{ rects: object[] }} node */
        selectNodeContents(node) {
          selected = node;
        },
        /** @param {{ rects: object[] }} node */
        selectNode(node) {
          selected = node;
        },
        getClientRects: () => selected.rects,
      };
    },
  },
});

/** @type {{ firstLineBox: (el: object) => object | null }} */
const { firstLineBox } = probe("devtools/probes/check_print_layout/layout_helpers.js")(
  probe("devtools/probes/check_print_layout/naming.js")(),
);
process.stdout.write(JSON.stringify(firstLineBox(el)));
