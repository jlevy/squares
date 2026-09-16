// Inline code against the text around it, for every visible `code` outside a `pre`: its
// baseline against the surrounding one, measured between two zero-size inline-blocks, one
// appended inside the code and one placed after it; the flat-bottomed ink below the baseline
// of `Hnx` in each font, measured on a canvas; and the chip's paint, type and wrapping.
//
// Takes whether to mark crops: with `true`, the first block holding prose code and the first
// holding supporting code are marked with `data-squares-code-crop`.
/** @param {boolean} crops */
(crops) => {
  const selected = new Set();
  const canvas = document.createElement("canvas");
  const context = /** @type {CanvasRenderingContext2D} */ (canvas.getContext("2d"));
  /** @param {CSSStyleDeclaration} style */
  const inkBottom = (style) => {
    context.font = `${style.fontStyle} ${style.fontWeight} ${style.fontSize} ${style.fontFamily}`;
    return context.measureText("Hnx").actualBoundingBoxDescent;
  };
  const marker = () => {
    const span = document.createElement("span");
    span.style.cssText =
      "display:inline-block;width:0;height:0;padding:0;margin:0;" +
      "border:0;line-height:0;vertical-align:baseline;visibility:hidden;";
    return span;
  };
  return [
    .../** @type {NodeListOf<HTMLElement>} */ (document.querySelectorAll("code:not(pre code)")),
  ].flatMap((code) => {
    const style = getComputedStyle(code);
    if (!code.getClientRects().length || style.visibility !== "visible") {
      return [];
    }
    const surrounding = getComputedStyle(/** @type {Element} */ (code.parentElement));
    if (crops) {
      const role = code.closest(".kpress-figcaption, .kpress-footnotes") ? "support" : "prose";
      if (!selected.has(role)) {
        /** @type {HTMLElement} */ (
          code.closest("p") || code.parentElement
        ).dataset.squaresCodeCrop = role;
        selected.add(role);
      }
    }
    const inner = marker(),
      outer = marker();
    code.append(inner);
    code.after(outer);
    const offset = inner.getBoundingClientRect().top - outer.getBoundingClientRect().top;
    inner.remove();
    outer.remove();
    const role = code.closest(".kpress-figcaption, .kpress-footnotes") ? "support" : "prose";
    return [
      {
        role,
        source: code.textContent,
        family: style.fontFamily,
        context_family: surrounding.fontFamily,
        weight: style.fontWeight,
        color: style.color,
        context_color: surrounding.color,
        size: parseFloat(style.fontSize),
        context_size: parseFloat(surrounding.fontSize),
        background_color: style.backgroundColor,
        border_styles: [
          style.borderTopStyle,
          style.borderRightStyle,
          style.borderBottomStyle,
          style.borderLeftStyle,
        ],
        border_widths: [
          style.borderTopWidth,
          style.borderRightWidth,
          style.borderBottomWidth,
          style.borderLeftWidth,
        ].map(parseFloat),
        white_space: style.whiteSpace,
        overflow_wrap: style.overflowWrap,
        word_break: style.wordBreak,
        baseline_offset: offset,
        ink_bottom: inkBottom(style),
        context_ink_bottom: inkBottom(surrounding),
        padding_top: parseFloat(style.paddingTop),
        padding_bottom: parseFloat(style.paddingBottom),
      },
    ];
  });
};
