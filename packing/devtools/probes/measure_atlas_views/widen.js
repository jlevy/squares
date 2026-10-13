// Lift the cap on the atlas block's width (`--site-wide`, the stylesheet's
// `--site-bleed-max`), so in a window wide enough the triangle's longest row stands whole
// instead of panning in its frame. The page's own resize handling lays the tiles out again.
() => {
  const grid = document.querySelector("[data-atlas-grid]");
  if (grid instanceof HTMLElement) {
    grid.style.setProperty("--site-wide", "100000px");
  }
};
