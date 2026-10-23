// The drawn rows of a following triangle and the script's own reading: each shown row's
// top on the stage and its tiles' left and right ends from the stage's left, the stage's
// height, the page's height and the window's, all as drawn now.
() => {
  const block = document.querySelector("[data-atlas-grid]");
  const cells = block?.querySelector(".site-atlas-cells");
  if (!(block instanceof HTMLElement) || !(cells instanceof HTMLElement)) {
    return null;
  }
  const box = cells.getBoundingClientRect();
  const rows = [...cells.querySelectorAll(".site-atlas-row")]
    .filter((row) => row.closest("[hidden]") === null)
    .map((row) => {
      const segments = [...row.querySelectorAll(".site-atlas-segment")]
        .map((segment) => segment.getBoundingClientRect())
        .filter((segment) => segment.width > 0);
      return {
        top: row.getBoundingClientRect().top - box.top,
        left: Math.min(...segments.map((segment) => segment.left)) - box.left,
        right: Math.max(...segments.map((segment) => segment.right)) - box.left,
      };
    });
  return {
    rows,
    reading: block.atlasFollow ?? null,
    follow: block.dataset.atlasFollow ?? null,
    zoomed: block.hasAttribute("data-atlas-zoom"),
    stage: box.height,
    page: document.documentElement.scrollHeight,
    window: window.innerHeight,
    scrollY: window.scrollY,
  };
};
