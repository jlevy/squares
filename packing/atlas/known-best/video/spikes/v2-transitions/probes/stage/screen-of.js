// Where one square sits on the screen, through the same matrix the page's own handler uses,
// so a gesture driven at these coordinates is the gesture and not a call dressed up as one.
// o.index is the square.
(o) => {
  const g = document.getElementById('world');
  const m = g.getScreenCTM();
  const p = window.atlasTransitions.poseOf(o.index);
  const q = new DOMPoint(p[0], p[1]).matrixTransform(m);
  return [q.x, q.y];
}
