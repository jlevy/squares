// The box tree KaTeX's internal `__renderToDomTree` returns before it is drawn, which
// `compare_math_fonts`'s advance probe sums. The `katex` global itself is in
// `probes/explainer.d.ts`.

/** One node of KaTeX's box tree: a symbol carries its text and metric widths. */
interface CompareMathFontsKatexNode {
  text?: unknown;
  width?: unknown;
  italic?: number;
  children?: CompareMathFontsKatexNode[];
}

/** The root of a tree `__renderToDomTree` builds, which draws itself as a DOM node. */
interface CompareMathFontsKatexTree extends CompareMathFontsKatexNode {
  toNode(): Node;
}
