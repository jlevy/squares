// `check_print_layout/layout_helpers.js`'s `firstLineBox` over Chrome's print rectangles from
// Further Reading, relative to the list item's top: a footnote reference whose ink reaches
// above the line. Its computed `line-height` is the argument; at `0px` it is an overlay
// whose rectangles are removed, and at any other height it is an inline that contributes.
// Prints the line box.
//
//   node zero-line-height-footnote.mjs <line-height>
import { probe } from "../probe.mjs";

const lineHeight = process.argv[2];
const reference = {
  lineHeight,
  rects: [
    {
      top: -8.515625,
      bottom: 13.484375,
      height: 22,
      width: 10.390625,
      left: 519.625,
      right: 530.015625,
    },
    {
      top: -8.515625,
      bottom: 13.484375,
      height: 22,
      width: 6.40625,
      left: 520.421875,
      right: 526.828125,
    },
  ],
};
const el = {
  querySelectorAll: () => [reference],
  rects: [
    { top: 0, bottom: 20, height: 20, width: 462.03125, left: 57.59375, right: 519.625 },
    ...reference.rects,
    { top: 21.25, bottom: 41.25, height: 20, width: 200, left: 57.59375, right: 257.59375 },
  ],
};
Object.assign(globalThis, {
  /** @param {{ lineHeight?: string }} node */
  getComputedStyle: (node) => ({ lineHeight: node.lineHeight }),
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
