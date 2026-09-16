// The build's scaling oracle on real linear and fixed-pixel geometry: the slot measurement's
// `linearGeometry` on a monospace `#base`, then under the two conditions it must refuse,
// hinted metrics and a fixed padding that does not scale with the font. `measureMath` is
// `measure_math.js`'s function, handed in as a handle.
/** @param {{ measureMath: SquaresMeasureMath }} o */
(o) => {
  const measure = o.measureMath.linearGeometry;
  const base = /** @type {HTMLElement} */ (document.querySelector("#base"));
  const positive = measure(base);
  /** @type {Record<string, { measurement?: SquaresLinearGeometry, error: string | null }>} */
  const controls = {};
  for (const [name, property, value] of /** @type {const} */ ([
    ["hinted_metrics", "textRendering", "auto"],
    ["nonlinear_scaling", "paddingLeft", "8px"],
  ])) {
    const old = base.style[property];
    base.style[property] = value;
    try {
      controls[name] = { measurement: measure(base), error: null };
    } catch (error) {
      controls[name] = { error: String(error) };
    } finally {
      base.style[property] = old;
    }
  }
  return { positive, controls };
};
