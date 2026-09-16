// Every visible formula's outer em against the text around it, which is the first ancestor
// that is not one of the math wrappers. Script sizes are KaTeX's own business and are not
// read. An inline caption formula also has its baseline measured against the caption's,
// between two zero-size inline-blocks; a prepared one is measured a second time with its
// fixed boxes unwrapped, on a copy swapped in and back out.
//
// Takes `{wrappers, crops}`: the selector list of math wrappers (`MATH_WRAPPERS`), and
// whether to mark the first block of each role with `data-squares-typography-crop`.
/** @param {{ wrappers: string, crops: boolean }} o */
({ wrappers, crops }) => {
  const selected = new Set();
  /** @type {TypographyMathContext[]} */
  const rows = [];
  const marker = () => {
    const span = document.createElement("span");
    span.style.cssText =
      "display:inline-block;width:0;height:0;padding:0;margin:0;" +
      "border:0;line-height:0;vertical-align:baseline;visibility:hidden;";
    return span;
  };
  /**
   * @param {Element} math
   * @param {Element} wrapper
   */
  const baseline = (math, wrapper) => {
    const last = [...math.querySelectorAll(".katex-html .base")].at(-1);
    if (!last) {
      return null;
    }
    const inner = marker(),
      outer = marker();
    last.append(inner);
    wrapper.after(outer);
    const offset = inner.getBoundingClientRect().top - outer.getBoundingClientRect().top;
    inner.remove();
    outer.remove();
    return offset;
  };
  for (const math of document.querySelectorAll(".katex")) {
    if (
      !math.getClientRects().length ||
      getComputedStyle(math).visibility !== "visible" ||
      math.closest("[hidden]")
    ) {
      continue;
    }
    let context = math.parentElement;
    while (context?.matches(`${wrappers}, .katex-display`)) {
      context = context.parentElement;
    }
    if (!context) {
      continue;
    }
    const display = !!math.closest(".katex-display, .tex-d, .kpress-math-display");
    const role = math.closest(".kpress-figcaption") ? "caption" : display ? "display" : "inline";
    const style = getComputedStyle(math),
      surrounding = getComputedStyle(context);
    /** @type {TypographyMathContext} */
    const row = {
      role,
      display_math: display,
      source: math.querySelector("annotation")?.textContent || math.textContent,
      size: parseFloat(style.fontSize),
      context_size: parseFloat(surrounding.fontSize),
      family: style.fontFamily,
      context_family: surrounding.fontFamily,
      weight: style.fontWeight,
      context_weight: surrounding.fontWeight,
      text_rendering: style.textRendering,
      context_text_rendering: surrounding.textRendering,
    };
    if (role === "caption" && !display) {
      row.caption = /** @type {Element} */ (math.closest(".kpress-figcaption")).textContent
        .trim()
        .slice(0, 180);
      row.baseline_prepared = !!math.closest('[data-kpress-math-prepared="true"]');
      let wrapper = math;
      while (wrapper.parentElement?.matches(wrappers)) {
        wrapper = wrapper.parentElement;
      }
      row.baseline_offset = baseline(math, wrapper);
      if (row.baseline_prepared) {
        const copy = /** @type {Element} */ (wrapper.cloneNode(true));
        copy.removeAttribute("data-kpress-math-prepared");
        copy.removeAttribute("data-squares-math-key");
        copy.querySelectorAll("[data-kpress-math-prepared]").forEach((element) => {
          element.removeAttribute("data-kpress-math-prepared");
        });
        for (const box of copy.querySelectorAll(".squares-math-box")) {
          const base = /** @type {HTMLElement} */ (box.firstElementChild);
          for (const property of /** @type {const} */ (["position", "left", "top"])) {
            base.style[property] = "";
          }
          box.replaceWith(base);
        }
        wrapper.replaceWith(copy);
        const candidate = copy.matches(".katex")
          ? copy
          : [...copy.querySelectorAll(".katex")].find((element) => element.getClientRects().length);
        row.unboxed_baseline_offset = candidate ? baseline(candidate, copy) : null;
        copy.replaceWith(wrapper);
      }
    }
    rows.push(row);
    if (crops && !selected.has(role)) {
      const block = /** @type {HTMLElement} */ (
        math.closest("p, figcaption, .tex-d, .kpress-math-display") || context
      );
      block.dataset.squaresTypographyCrop = role;
      selected.add(role);
    }
  }
  return rows;
};
