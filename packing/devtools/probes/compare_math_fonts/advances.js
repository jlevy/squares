// Draw each input into the page and read back both numbers: the advance the browser
// actually inked, and the width KaTeX summed from its own table to place it. Both come
// from one call, on the page's own KaTeX build, inside the column so that the rules and
// the size the page sets are the ones in force -- a measurement taken in a bare document
// would compare fonts nobody is looking at.
/** @param {string[]} inputs */
(inputs) => {
  const column = /** @type {Element} */ (document.querySelector(".kpress"));
  const host = document.createElement("span");
  column.appendChild(host);
  const measured = [];
  try {
    for (const input of inputs) {
      host.textContent = "";
      const tree = katex.__renderToDomTree(input, { throwOnError: true, displayMode: false });
      host.appendChild(tree.toNode());
      const drawn = /** @type {Element} */ (host.firstElementChild);
      const size = parseFloat(getComputedStyle(drawn).fontSize);
      measured.push({
        input,
        /* The sum of the leaves' own boxes: KaTeX's table is per glyph, and what it
           places is the run, so the run is what compares with the drawn advance. */
        metric: leaves(tree),
        drawn: drawn.getBoundingClientRect().width / size,
      });
    }
  } finally {
    host.remove();
  }
  return measured;

  /* A symbol's box is its advance plus its italic correction, because that is what
     KaTeX draws: `SymbolNode.toNode` puts the correction on the node as a right margin,
     and an inline margin widens the box the browser reports for the run around it. The
     two numbers are separate rows in the metric table and the patch rewrites both. */
  /**
   * @param {CompareMathFontsKatexNode} node
   * @returns {number}
   */
  function leaves(node) {
    if (typeof node.width === "number" && typeof node.text === "string") {
      if ([...node.text].length > 1) {
        throw new Error(
          "KaTeX merged " +
            JSON.stringify(node.text) +
            " into one node, whose declared " +
            "width is only its first character: pick a single-character input",
        );
      }
      return node.width + (node.italic || 0);
    }
    return (node.children || []).reduce((sum, child) => sum + leaves(child), 0);
  }
};
