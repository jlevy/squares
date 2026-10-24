// Scroll the page until a following triangle reads `to` pixels of scroll since its stage
// was pinned, and let two frames pass; the scroll it then reads, or null with no reading.
async (/** @type {{to: number}} */ { to }) => {
  const block = document.querySelector("[data-atlas-grid]");
  if (!(block instanceof HTMLElement) || block.atlasFollow === undefined) {
    return null;
  }
  window.scrollBy({ top: to - block.atlasFollow.scrolled, behavior: "instant" });
  await new Promise((resolve) => requestAnimationFrame(() => requestAnimationFrame(resolve)));
  return block.atlasFollow.scrolled;
};
