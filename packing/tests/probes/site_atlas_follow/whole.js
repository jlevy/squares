// The first of the tiles for cases `cases` that a following triangle draws whole where
// the window shows the stage: its case and the window point at its middle, where a
// pointer presses it; null when none is.
(/** @type {{cases: number[]}} */ { cases }) => {
  const cells = document.querySelector("[data-atlas-grid] .site-atlas-cells");
  if (!(cells instanceof HTMLElement)) {
    return null;
  }
  const stage = cells.getBoundingClientRect();
  for (const n of cases) {
    const tile = cells.querySelector(`.site-atlas-cell[data-atlas-n="${n}"]`);
    if (!(tile instanceof HTMLElement)) {
      continue;
    }
    const drawn = tile.getBoundingClientRect();
    if (
      drawn.left >= Math.max(stage.left, 0) &&
      drawn.right <= Math.min(stage.right, window.innerWidth) &&
      drawn.top >= Math.max(stage.top, 0) &&
      drawn.bottom <= Math.min(stage.bottom, window.innerHeight)
    ) {
      return { n, x: drawn.left + drawn.width / 2, y: drawn.top + drawn.height / 2 };
    }
  }
  return null;
};
