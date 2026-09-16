// The lowest point the packing drawing reaches through one step, in stage units, counting only
// what the SVG draws. That is every shape under `#world` that is displayed, visible and painted
// (the squares, the box, its trace, and any mark or link on show), with half its stroke, cut at
// the SVG's own floor when the SVG clips its overflow, as `#packing-svg` does. An element's box
// is not what is drawn: the undrawn `#container`, a trace faded out and a square not yet arrived
// all have one, and a square swinging past the view is cut flat at the SVG's edge.
// o.n is the step's n and o.style the style; 97 evenly spaced instants are sampled. Answers the
// deepest point, the SVG's floor, and whether the SVG clips there.
/** @param {{n: number, style: import("../../src/api/workbench-api.js").AtlasStyle}} o */
(o) => {
  const api = window.atlasTransitions;
  api.setStyle(o.style);
  api.setStepN(o.n);
  const stage = /** @type {HTMLElement} */ (
    document.getElementById("stage")
  ).getBoundingClientRect();
  const svg = /** @type {Element} */ (document.getElementById("packing-svg"));
  const scale = stage.width / 1920;
  const floor = (svg.getBoundingClientRect().bottom - stage.top) / scale;
  const clips = ["hidden", "clip", "scroll", "auto"].includes(getComputedStyle(svg).overflowY);
  /** @param {Element} shape */
  const halfStroke = (shape) => {
    const style = getComputedStyle(shape);
    let opacity = 1;
    for (let node = /** @type {Element | null} */ (shape); node && node !== svg; ) {
      const own = getComputedStyle(node);
      if (own.display === "none") {
        return null;
      }
      opacity *= Number(own.opacity);
      node = node.parentElement;
    }
    const width = Number.parseFloat(style.strokeWidth);
    const stroked = style.stroke !== "none" && Number(style.strokeOpacity) > 0 && width > 0;
    const filled = style.fill !== "none" && Number(style.fillOpacity) > 0;
    if (style.visibility !== "visible" || !(opacity > 0) || !(stroked || filled)) {
      return null;
    }
    if (!stroked) {
      return 0;
    }
    // A non-scaling stroke is as wide in the SVG's own pixels, which are stage units; any other
    // is as wide in user units, scaled by the shape's matrix to the screen and back to the stage.
    const matrix = /** @type {SVGGraphicsElement} */ (shape).getScreenCTM();
    const toStage =
      style.vectorEffect === "non-scaling-stroke" || matrix === null
        ? 1
        : Math.hypot(matrix.a, matrix.b) / scale;
    return (width * toStage) / 2;
  };
  const shapes = svg.querySelectorAll(
    "#world :is(rect, path, line, polygon, polyline, circle, ellipse, text, use)",
  );
  const total = api.duration();
  let deepest = -Infinity;
  for (let k = 0; k <= 96; k++) {
    api.seek((total * k) / 96);
    for (const shape of shapes) {
      const r = shape.getBoundingClientRect();
      const half = r.width > 0 || r.height > 0 ? halfStroke(shape) : null;
      if (half === null) {
        continue;
      }
      const top = (r.top - stage.top) / scale - half;
      const bottom = (r.bottom - stage.top) / scale + half;
      if (clips && top >= floor) {
        continue;
      }
      deepest = Math.max(deepest, clips ? Math.min(bottom, floor) : bottom);
    }
  }
  return { deepest, floor, clips };
};
