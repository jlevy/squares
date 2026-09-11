// Does style A come to rest in the same poses with the snap off and on? Takes {index}.
(o) => {
  const A = window.atlasTransitions;
  A.select(o.index);
  A.setStyle("tween");
  A.setSnap(false);
  A.seek(A.duration());
  const free = Array.from(document.querySelectorAll("#squares g"))
    .filter((g) => g.style.display !== "none")
    .map((g) => g.getAttribute("transform"));
  A.setSnap(true);
  A.seek(A.duration());
  const snap = Array.from(document.querySelectorAll("#squares g"))
    .filter((g) => g.style.display !== "none")
    .map((g) => g.getAttribute("transform"));
  return JSON.stringify(free) === JSON.stringify(snap);
};
