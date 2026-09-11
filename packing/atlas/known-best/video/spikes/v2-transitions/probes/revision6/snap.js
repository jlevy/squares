// What the snapped and the free run miss by, and whether they rest in the same poses.
// Takes {index, style}.
(o) => {
  const A = window.atlasTransitions;
  A.select(o.index);
  A.setStyle(o.style);
  A.setBlind(false);
  const snap = A.physics(o.index, o.style, "snap"),
    free = A.physics(o.index, o.style, "free");
  A.setSnap(false);
  A.seek(A.duration());
  const note = String(A.gapBar().side);
  const poses = Array.from(document.querySelectorAll("#squares g"))
    .filter((g) => g.style.display !== "none")
    .map((g) => g.getAttribute("transform"));
  A.setSnap(true);
  A.seek(A.duration());
  const snapped = Array.from(document.querySelectorAll("#squares g"))
    .filter((g) => g.style.display !== "none")
    .map((g) => g.getAttribute("transform"));
  return {
    snapMiss: snap.miss,
    freeMiss: free.miss,
    note,
    same: JSON.stringify(poses) === JSON.stringify(snapped),
  };
};
