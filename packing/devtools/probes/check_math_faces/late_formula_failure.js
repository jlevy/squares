// Self-test: the first paint was ready, but a later formula appeared before its glyph fonts.
() => {
  /** @type {SquaresFontRequirement} */ (
    /** @type {SquaresMathFirstPaint} */ (__mathFirstPaint).required[0]
  ).ready = true;
  /** @type {SquaresMathLoadingState} */ (__mathLoadingState).unreadyMath.push("late expression");
};
