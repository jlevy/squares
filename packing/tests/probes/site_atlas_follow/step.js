// Scroll the page `by` pixels, as one turn of a reader's wheel does, and let two frames
// pass, so the atlas's following has run on the new position before it is read. Says
// whether the page has reached either end or the atlas has passed above the window.
async (/** @type {{by: number}} */ { by }) => {
  window.scrollBy({ top: by, behavior: "instant" });
  await new Promise((resolve) => requestAnimationFrame(() => requestAnimationFrame(resolve)));
  const cells = document.querySelector("[data-atlas-grid] .site-atlas-cells");
  const bottom = document.documentElement.scrollHeight - window.innerHeight;
  return {
    top: window.scrollY <= 0,
    end: window.scrollY >= bottom - 1,
    past: cells instanceof HTMLElement && cells.getBoundingClientRect().bottom < 0,
  };
};
