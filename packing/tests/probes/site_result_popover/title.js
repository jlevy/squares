/** @param {string} id */
(id) => {
  const popover = document.getElementById(id);
  if (!popover) {
    throw new Error("The result dialog is missing");
  }
  const article = popover.querySelector("article.site-result");
  const heading = article?.querySelector("h1");
  const namedBy = popover.getAttribute("aria-labelledby");
  const named = [...document.querySelectorAll("[id]")].filter((element) => element.id === namedBy);
  const ids = [...document.querySelectorAll("[id]")].map((element) => element.id);
  const duplicates = [...new Set(ids.filter((value, index) => ids.indexOf(value) !== index))];
  const outer = [...popover.children].filter((element) =>
    element.matches(".site-card-label, .site-popover-value"),
  );
  const visible = [...outer, ...(heading ? [heading] : [])].filter(
    (element) =>
      element.getClientRects().length > 0 && getComputedStyle(element).visibility !== "hidden",
  );
  return {
    titleCount: visible.length,
    title: heading?.textContent ?? null,
    titleID: heading?.id ?? null,
    namedBy,
    namedCount: named.length,
    namedInside: named.length === 1 && popover.contains(named[0] ?? null),
    namedText: named[0]?.textContent ?? null,
    duplicateIDs: duplicates,
    outerTitles: outer.length,
    math: [...(heading?.querySelectorAll(".kpress-math-semantic mi") ?? [])].map(
      (element) => element.textContent,
    ),
    mathTransforms: [
      ...(heading?.querySelectorAll(".kpress-math-render, .kpress-math-semantic math") ?? []),
    ].map((element) => getComputedStyle(element).textTransform),
  };
};
