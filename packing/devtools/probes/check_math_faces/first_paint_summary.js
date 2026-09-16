// What `check_math_loading/first_paint` recorded of the first mathematics paint: when, how
// many faces were declared, the required glyph runs, and how many glyph font checks ran.
() =>
  globalThis.__mathFirstPaint && {
    at: globalThis.__mathFirstPaint.at,
    faces: globalThis.__mathFirstPaint.faces.length,
    required: globalThis.__mathFirstPaint.required,
    math_font_checks: /** @type {SquaresMathLoadingState} */ (globalThis.__mathLoadingState)
      .mathFontChecks,
  };
