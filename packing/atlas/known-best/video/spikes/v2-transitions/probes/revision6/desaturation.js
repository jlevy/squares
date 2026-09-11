// The fills at the dwell, mid move and at rest, with the drain on and then off.
// Takes {index, style}.
(o) => {
  const A = window.atlasTransitions;
  A.stopAll();
  A.select(o.index);
  A.setStyle(o.style);
  A.setSnap(true);
  A.setBlind(false);
  const fills = () =>
    Array.from(document.querySelectorAll("#squares g"))
      .filter((g) => g.style.display !== "none")
      .map((g) => g.firstElementChild.getAttribute("fill"));
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
