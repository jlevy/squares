// Whether the atlas's tiles stand whole in their frame, with no row reaching past it to
// be panned to.
() => {
  const cells = document.querySelector(".site-atlas-cells");
  return cells instanceof HTMLElement && cells.scrollWidth <= cells.clientWidth;
};
