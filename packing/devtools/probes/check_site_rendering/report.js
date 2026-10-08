// A single layout read after load and font settlement, followed by scroll sampling.
() => {
  /** @type {{supported: boolean, cls: number, lcpMs: number, longestTaskMs: number, blockingMs: number, shifts: number} | undefined} */
  const timing = Reflect.get(window, "siteRenderingMeasure");
  const math = [...document.querySelectorAll(".kpress-math, .tex, .tex-d")].filter(
    (element) => !element.parentElement?.closest(".kpress-math, .tex, .tex-d"),
  );
  const shown = math.filter((element) => element.getClientRects().length);
  const unreadable = shown.filter((element) => {
    const visual = [...element.querySelectorAll(".katex-html")].find(
      (node) => node.getClientRects().length && getComputedStyle(node).visibility !== "hidden",
    );
    return !visual;
  });
  const article = document.querySelector("article, main");
  const h1 = document.querySelector("h1");
  const figures = [...document.querySelectorAll("main img, article img")];
  return {
    ...timing,
    contentChars: article?.textContent?.trim().length ?? 0,
    heading: h1?.textContent?.trim() ?? "",
    shownMath: shown.length,
    unreadableMath: unreadable.length,
    unreservedImages: figures.filter(
      (image) => !image.hasAttribute("width") || !image.hasAttribute("height"),
    ).length,
    pending: document.querySelectorAll("[data-kpress-math-pending]").length,
  };
};
