// What `check_print_layout`'s probes pass between them and return: the element naming both
// passes share, the helpers the layout probe is composed from, and the rows it measures.
// Mirrors the `TypedDict`s in `check_print_layout.py`.

/** `naming.js`: how every row names an element, and the precision it reports at. */
interface PrintLayoutNaming {
  sig(el: Element): string;
  round(v: number): number;
}

/** `layout_helpers.js`: the pieces of the layout probe the Node tests run on their own. */
interface PrintLayoutHelpers {
  bulletBox(li: Element, before: CSSStyleDeclaration): PrintLayoutBullet | null;
  firstLineBox(el: Element): { top: number; bottom: number } | null;
  widestRun(root: Element): PrintLayoutOverflow | null;
  inkRight(el: Element): number;
}

interface PrintLayoutCentred {
  index: number;
  parent: number;
  path: string;
  align: string;
  declared: boolean;
  shown: boolean;
}

interface PrintLayoutMarker {
  path: string;
  markerCentre: number;
  lineCentre: number;
  fontSize: number;
  baseFontSize: number;
  lineHeight: number;
  width: number;
  height: number;
  painted: boolean;
}

interface PrintLayoutBullet {
  path: string;
  width: number;
  height: number;
  painted: boolean;
}

interface PrintLayoutFootnote {
  path: string;
  text: string;
  leadIn: number;
  fontSize: number;
}

interface PrintLayoutBoxed {
  path: string;
  text: string;
  offset: number;
}

interface PrintLayoutOverflow {
  path: string;
  over: number;
  text: string;
}

/** `layout.js`: everything one pass measures, plus the column it measured at. */
interface PrintLayoutProbe {
  centred: PrintLayoutCentred[];
  markers: PrintLayoutMarker[];
  bullets: PrintLayoutBullet[];
  footnotes: PrintLayoutFootnote[];
  boxed: PrintLayoutBoxed[];
  overflow: PrintLayoutOverflow[];
  pageOverflow: number;
  widest: PrintLayoutOverflow | null;
  measure: number;
  viewport: number;
}

/** `self_check_defects.js`: the overflow and the stretched bullet `--self-check` injects. */
interface PrintLayoutSelfCheckSpec {
  over: number;
  name: string;
  bullet: string;
}
