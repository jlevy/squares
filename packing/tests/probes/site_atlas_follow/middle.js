// Where tile `n` is drawn across the stage: the case, how far its middle stands right of
// the middle of the stage, and its width. With no `n`, the tile nearest the middle of the
// stage on the focus line of a following triangle, the one the reader is looking at.
(/** @type {{n: number | null}} */ { n }) => {
  const block = document.querySelector("[data-atlas-grid]");
  const cells = block?.querySelector(".site-atlas-cells");
  if (!(block instanceof HTMLElement) || !(cells instanceof HTMLElement)) {
    return null;
  }
  const box = cells.getBoundingClientRect();
  const middle = box.left + cells.clientWidth / 2;
  const line = box.top + (block.atlasFollow?.line ?? 0);
  const tiles = [...cells.querySelectorAll(".site-atlas-cell")].filter(
    (tile) =>
      tile instanceof HTMLElement &&
      tile.closest("[hidden]") === null &&
      (n === null || tile.dataset.atlasN === String(n)),
  );
  /** @param {Element} tile */
  const apart = (tile) => {
    const drawn = tile.getBoundingClientRect();
    return Math.hypot(drawn.left + drawn.width / 2 - middle, drawn.top + drawn.height / 2 - line);
  };
  const nearest = tiles.reduce(
    (best, tile) => (best === null || apart(tile) < apart(best) ? tile : best),
    /** @type {Element | null} */ (null),
  );
  if (!(nearest instanceof HTMLElement)) {
    return null;
  }
  const drawn = nearest.getBoundingClientRect();
  return {
    n: Number(nearest.dataset.atlasN),
    offset: drawn.left + drawn.width / 2 - middle,
    width: drawn.width,
  };
};
