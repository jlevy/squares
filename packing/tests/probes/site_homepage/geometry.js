// Actual SVG drawing bounds and the HTML link above that same native card.
/** @param {number} n */
(n) => {
  const grid = document.querySelector("[data-atlas-preview]");
  const link = grid?.querySelector(`a[data-case="${n}"]`);
  const svg = link?.querySelector("[data-homepage-atlas-svg]");
  const drawing = svg?.querySelector(`g[data-n="${n}"] rect[data-feature="container-outline"]`);
  if (!(svg instanceof SVGSVGElement) || !link || !drawing || !(grid instanceof HTMLElement)) {
    throw new Error(`Missing native Atlas card ${n}`);
  }
  const overlay = link.getBoundingClientRect();
  const outline = drawing.getBoundingClientRect();
  const crop = svg.getBoundingClientRect();
  const scale = svg.getBoundingClientRect().width / svg.viewBox.baseVal.width;
  return {
    n,
    scale,
    left_gap: (outline.left - crop.left) / scale,
    top_gap: (outline.top - crop.top) / scale,
    link_width: crop.width / scale,
    link_height: crop.height / scale,
    contained:
      crop.left >= overlay.left &&
      crop.right <= overlay.right &&
      crop.top >= overlay.top &&
      crop.bottom <= overlay.bottom,
    drawing_width: outline.width / scale,
    drawing_height: outline.height / scale,
    horizontal_scroll: grid.scrollLeft,
    center_x: (overlay.left + overlay.right) / 2,
    viewport_width: window.innerWidth,
  };
};
