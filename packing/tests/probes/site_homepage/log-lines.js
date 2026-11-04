// A page's day log with every day opened: each element that runs out of its day's box,
// and how the links that open a line wrap, a result's id against the rest.
async () => {
  await document.fonts.ready;
  const log = document.querySelector(".site-rollup.site-added");
  const blocks = [...(log?.querySelectorAll(":scope > details") ?? [])];
  for (const block of blocks) {
    if (block instanceof HTMLDetailsElement) {
      block.open = true;
    }
  }
  await new Promise((resolve) => requestAnimationFrame(() => resolve(undefined)));
  const outside = blocks.flatMap((block) => {
    const frame = block.getBoundingClientRect();
    return [...block.querySelectorAll("*")]
      .filter(
        (element) =>
          element.checkVisibility({ visibilityProperty: true }) &&
          [...element.getClientRects()].some(
            (rect) =>
              rect.width > 0 && (rect.left < frame.left - 0.5 || rect.right > frame.right + 0.5),
          ),
      )
      .map(
        (element) =>
          `${block.getAttribute("data-day")}: ${element.textContent?.trim().slice(0, 60)}`,
      );
  });
  const openers = [...(log?.querySelectorAll("li > a:first-child") ?? [])];
  /** @param {Element} link */
  const wrapping = (link) => {
    const style = getComputedStyle(link);
    return { white_space: style.whiteSpace, numerals: style.fontVariantNumeric };
  };
  return {
    days: blocks.length,
    open: blocks.filter((block) => block instanceof HTMLDetailsElement && block.open).length,
    lines: log?.querySelectorAll("li").length ?? 0,
    outside,
    ids: openers.filter((link) => link.matches(".site-rollup-id")).map(wrapping),
    others: openers.filter((link) => !link.matches(".site-rollup-id")).map(wrapping),
  };
};
