// The addressed diagram's final placement and focus, with or without scripts.
/** @param {number} n */
(n) => {
  const tile = document.getElementById(`atlas-n-${n}`);
  if (!(tile instanceof HTMLElement)) {
    throw new Error(`No Atlas tile for case ${n}`);
  }
  const box = tile.getBoundingClientRect();
  return {
    top: box.top,
    bottom: box.bottom,
    viewportHeight: innerHeight,
    focused: document.activeElement === tile,
    targeted: tile.matches(":target"),
    outlineWidth: getComputedStyle(tile).outlineWidth,
    shown: [...document.querySelectorAll(".site-atlas-cell")].filter(
      (cell) => cell.getBoundingClientRect().width > 0,
    ).length,
  };
};
