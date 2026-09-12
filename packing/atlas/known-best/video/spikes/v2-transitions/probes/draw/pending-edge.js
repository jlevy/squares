// The edge being drawn while the gesture is still being made.
() => {
  const l = document.getElementById("draw-line");
  return {
    shown: l.style.display !== "none",
    x1: Number(l.getAttribute("x1")),
    x2: Number(l.getAttribute("x2")),
  };
};
