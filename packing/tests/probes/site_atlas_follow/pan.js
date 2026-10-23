// The reader pans the triangle by hand, `by` pixels toward its right end, and the next
// frame passes.
async (/** @type {{by: number}} */ { by }) => {
  const cells = document.querySelector("[data-atlas-grid] .site-atlas-cells");
  if (!(cells instanceof HTMLElement)) {
    return false;
  }
  cells.scrollBy({ left: by, behavior: "instant" });
  await new Promise((resolve) => requestAnimationFrame(() => requestAnimationFrame(resolve)));
  return true;
};
