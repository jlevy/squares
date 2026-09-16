// Whether the field the figure restored is the one it rebuilds at the same direction: the
// canvas as restored, against the canvas after the figure's range control announces an
// input at an unchanged value. A stale direction bitmap differs.
/** @param {Element} figure */
(figure) => {
  const canvas = /** @type {HTMLCanvasElement} */ (figure.querySelector("canvas"));
  const restored = canvas.toDataURL();
  /** @type {Element} */ (figure.querySelector("input[type=range]")).dispatchEvent(
    new Event("input", { bubbles: true }),
  );
  return canvas.toDataURL() === restored;
};
