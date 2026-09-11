// Where one square sits on the screen, through the same matrix the page's own handler uses,
// so a gesture driven at these coordinates is the gesture and not a call dressed up as one.
// o.index is the square.
(o) => {
  // `getElementById` is declared as returning an HTMLElement, and `#world` is the stage's SVG
  // group, so the handle is widened to Element before it is named as the `<g>` it is.
  const g = /** @type {SVGGElement} */ (/** @type {Element} */ (document.getElementById("world")));
  const m = g.getScreenCTM();
  const p = window.atlasTransitions.poseOf(o.index);
  const q = new DOMPoint(p[0], p[1]).matrixTransform(m);
  return [q.x, q.y];
};
