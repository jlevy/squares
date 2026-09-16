// The fills at the dwell, mid move and at rest, with the drain on and then off.
// Takes {index, style}.
/** @param {{index: number, style: import("../../src/api/workbench-api.js").AtlasStyle}} o */
(o) => {
  const A = window.atlasTransitions;
  A.stopAll();
  A.select(o.index);
  A.setStyle(o.style);
  A.setSnap(true);
  A.setBlind(false);
  /** @param {Element} g */
  const fillOf = (g) => {
    const rect = g.firstElementChild;
    if (rect == null) {
      throw new Error("a drawn square has no rect");
    }
    return rect.getAttribute("fill");
  };
  const fills = () =>
    Array.from(/** @type {NodeListOf<SVGGElement>} */ (document.querySelectorAll("#squares g")))
      .filter((g) => g.style.display !== "none")
      .map((g) => fillOf(g));
  A.setDesaturate(true);
  A.seek(0.5);
  const dwellOn = fills();
  A.seek(1.7);
  const midOn = fills();
  A.seek(A.duration());
  const restOn = fills();
  A.setDesaturate(false);
  A.seek(0.5);
  const dwellOff = fills();
  A.seek(1.7);
  const midOff = fills();
  A.seek(A.duration());
  const restOff = fills();
  A.setDesaturate(true);
  return { dwellOn, midOn, restOn, dwellOff, midOff, restOff };
};
