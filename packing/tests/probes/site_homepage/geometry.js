// The upstream square drawing and its canonical packing link after horizontal pan.
/** @param {number} n */
(n) => {
  const cells = document.querySelector("#homepage-atlas-cells");
  const link = cells?.querySelector(`a[data-case="${n}"]`);
  const image = link?.querySelector("img");
  if (!(cells instanceof HTMLElement) || !(image instanceof HTMLImageElement) || !link) {
    throw new Error(`Missing canonical Atlas drawing ${n}`);
  }
  const overlay = link.getBoundingClientRect();
  const drawing = image.getBoundingClientRect();
  return {
    n,
    contained:
      drawing.left >= overlay.left &&
      drawing.right <= overlay.right &&
      drawing.top >= overlay.top &&
      drawing.bottom <= overlay.bottom,
    drawing_width: drawing.width,
    drawing_height: drawing.height,
    source: image.getAttribute("src"),
    row: Number(link.closest("[data-atlas-row]")?.getAttribute("data-atlas-row")),
    segment: link.closest("[data-atlas-segment]")?.getAttribute("data-atlas-segment"),
    horizontal_scroll: cells.scrollLeft,
    page_overflow: document.documentElement.scrollWidth - document.documentElement.clientWidth,
    center_x: (overlay.left + overlay.right) / 2,
    viewport_width: window.innerWidth,
  };
};
