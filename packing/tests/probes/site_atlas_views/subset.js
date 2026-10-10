// Keep a real subset of the instance's canonical witness drawings. The next control
// change must derive Global's reference from these shown sides, never a corpus count.
(/** @type {{keep: number[]}} */ { keep }) => {
  const wanted = new Set(keep);
  for (const tile of document.querySelectorAll(".site-atlas-cell")) {
    if (!wanted.has(Number(tile.getAttribute("data-atlas-n")))) {
      tile.remove();
    }
  }
};
