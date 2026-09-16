// A prose bullet's measured optical alignment, saved beside its image: the drawn marker's
// box against the baseline of the item's first visible prose run, found by inserting a
// zero-size inline-block at that baseline. The run's rectangles are read before and after
// the insertion so the caller can refuse a measurement that moved the text it measured.
// Every math box in the item is listed with its clipping, for reading the image against.
//
// Takes the item's selector.
/** @param {string} selector */
(selector) => {
  const item = /** @type {Element} */ (document.querySelector(selector));
  const walker = document.createTreeWalker(item, NodeFilter.SHOW_TEXT);
  /** @type {Node | undefined} */
  let text;
  while (walker.nextNode()) {
    const node = walker.currentNode;
    if (
      /** @type {string} */ (node.textContent).trim() &&
      !(/** @type {Element} */ (node.parentElement).closest(".katex,math")) &&
      /** @type {Element} */ (node.parentElement).checkVisibility({ visibilityProperty: true })
    ) {
      text = node;
      break;
    }
  }
  const range = document.createRange();
  range.selectNodeContents(/** @type {Node} */ (text));
  const initialText = [...range.getClientRects()].map((rect) => rect.toJSON());
  const baseline = document.createElement("span");
  baseline.style.cssText =
    "display:inline-block;width:0;height:0;padding:0;" +
    "margin:0;line-height:0;vertical-align:baseline";
  /** @type {Element} */ (/** @type {Node} */ (text).parentElement).insertBefore(
    baseline,
    /** @type {Node} */ (text),
  );
  const y = baseline.getBoundingClientRect().top;
  const sampledText = [...range.getClientRects()].map((rect) => rect.toJSON());
  baseline.remove();
  const before = getComputedStyle(item, "::before"),
    box = item.getBoundingClientRect();
  const height = parseFloat(before.height),
    width = parseFloat(before.width);
  const top = box.top + parseFloat(before.top);
  const font = getComputedStyle(/** @type {Element} */ (/** @type {Node} */ (text).parentElement)),
    fontSize = parseFloat(font.fontSize);
  return {
    content: before.content,
    width,
    height,
    top,
    centre: top + height / 2,
    baseline: y,
    fontSize,
    aboveBaselineEm: (y - top - height / 2) / fontSize,
    initialText,
    sampledText,
    item: box.toJSON(),
    fontFamily: font.fontFamily,
    fontWeight: font.fontWeight,
    math: [
      ...item.querySelectorAll(
        ".kpress-math, .katex, .katex-mathml, .katex-html, .squares-math-box, .base, math",
      ),
    ].map((node) => {
      const style = getComputedStyle(node),
        range = document.createRange();
      range.selectNode(node);
      return {
        tag: node.tagName,
        classes: node.className,
        position: style.position,
        lineHeight: style.lineHeight,
        clip: style.clip,
        clipPath: style.clipPath,
        rects: [...range.getClientRects()].map((rect) => rect.toJSON()),
      };
    }),
  };
};
