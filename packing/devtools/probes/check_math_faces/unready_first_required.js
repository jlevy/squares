// Self-test: the first paint's required glyph run was not ready after all.
() => {
  /** @type {SquaresFontRequirement} */ (
    /** @type {SquaresMathFirstPaint} */ (__mathFirstPaint).required[0]
  ).ready = false;
};
