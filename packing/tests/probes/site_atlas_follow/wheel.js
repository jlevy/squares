// A trackpad turned sideways by `x` and down by `y` over the triangle: the page scrolls
// down as the wheel would scroll it, and the event reaches the triangle. Two frames pass.
async (/** @type {{x: number, y: number}} */ { x, y }) => {
  const cells = document.querySelector("[data-atlas-grid] .site-atlas-cells");
  if (!(cells instanceof HTMLElement)) {
    return false;
  }
  cells.dispatchEvent(new WheelEvent("wheel", { deltaX: x, deltaY: y, bubbles: true }));
  window.scrollBy({ top: y, behavior: "instant" });
  await new Promise((resolve) => requestAnimationFrame(() => requestAnimationFrame(resolve)));
  return true;
};
