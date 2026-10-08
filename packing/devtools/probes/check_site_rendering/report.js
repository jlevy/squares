// A single layout read after load and font settlement, followed by scroll sampling.
() => {
  /** @type {{supported: boolean, cls: number, lcpMs: number, longestTaskMs: number, blockingMs: number, shifts: number} | undefined} */
  const timing = Reflect.get(window, "siteRenderingMeasure");
  const math = [...document.querySelectorAll(".kpress-math, .tex, .tex-d")].filter(
    (element) => !element.parentElement?.closest(".kpress-math, .tex, .tex-d"),
  );
  /** @param {Element | null} element */
  const visible = (element) =>
    element instanceof HTMLElement &&
    element.getClientRects().length > 0 &&
    getComputedStyle(element).visibility !== "hidden";
  // Native collapsed sections may contain additional formulas. A hidden formula in
  // primary prose must fail rather than disappear from the no-JavaScript sample.
  const shown = math.filter((element) => {
    if (element.closest("[popover]:not(:popover-open)")) {
      return false;
    }
    const closed = element.closest("details:not([open])");
    if (closed && !element.closest("summary")) {
      return false;
    }
    const held = element.parentElement?.closest("[hidden]");
    return !held;
  });
  const unreadable = shown.filter((element) => {
    const visual = [...element.querySelectorAll(".katex-html")].find(
      (node) => node.getClientRects().length && getComputedStyle(node).visibility !== "hidden",
    );
    return !visible(element) || !visual;
  });
  const article = [...document.querySelectorAll("article, main")].find(visible);
  const h1 = [...document.querySelectorAll("h1")].find(visible);
  const figures = [...document.querySelectorAll("main img, article img")];
  return {
    ...timing,
    // biome-ignore lint/nursery/useDomNodeTextContent: the gate measures rendered readable text, excluding hidden content.
    contentChars: (article instanceof HTMLElement ? article.innerText : "").trim().length ?? 0,
    // biome-ignore lint/nursery/useDomNodeTextContent: a hidden heading must not pass the reading contract.
    heading: h1 instanceof HTMLElement ? h1.innerText.trim() : "",
    shownMath: shown.length,
    unreadableMath: unreadable.length,
    unreservedImages: figures.filter(
      (image) => !image.hasAttribute("width") || !image.hasAttribute("height"),
    ).length,
    pending: document.querySelectorAll("[data-kpress-math-pending]").length,
  };
};
