// `check_print_layout/layout_helpers.js`'s `bulletBox` over one unordered-list item whose
// `::before` computes a painted square, then that square stretched into a bar, missing, not
// displayed and not painted; then the square on an ordered-list item and on a hidden one.
// `sig` is a stand-in and `round` is `naming.js`'s own. Prints `{boxes, ordered, hidden}`.
import { probe } from "../probe.mjs";

const { round } = probe("devtools/probes/check_print_layout/naming.js")();
/** @type {{ bulletBox: (li: object, before: object) => object | null }} */
const { bulletBox } = probe("devtools/probes/check_print_layout/layout_helpers.js")({
  sig: () => "ul[0] > li[0]",
  round,
});

const item = { parentElement: { tagName: "UL" }, getClientRects: () => [{}] };
const square = {
  content: '""',
  display: "block",
  visibility: "visible",
  opacity: "1",
  backgroundColor: "rgb(10, 10, 10)",
  width: "3.3px",
  height: "3.3px",
};
const variants = [
  square,
  { ...square, height: "25px" },
  { ...square, content: "none", width: "auto", height: "auto" },
  { ...square, display: "none" },
  { ...square, backgroundColor: "rgba(0, 0, 0, 0)" },
];
process.stdout.write(
  JSON.stringify({
    boxes: variants.map((before) => bulletBox(item, before)),
    ordered: bulletBox({ ...item, parentElement: { tagName: "OL" } }, square),
    hidden: bulletBox({ ...item, getClientRects: () => [] }, square),
  }),
);
