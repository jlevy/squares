// Self-test: a first paint whose one required glyph run was ready, beside an unused face that
// never loaded, and a sampler that ran its glyph font check with no failures.
() => {
  globalThis.__mathFirstPaint = /** @type {SquaresMathFirstPaint} */ (
    /** @type {unknown} */ ({
      faces: [{ family: "KaTeX_Main", status: "unloaded", weight: "700" }],
      required: [{ spec: "16px serif", text: "x", ready: true }],
    })
  );
  globalThis.__mathLoadingState = /** @type {SquaresMathLoadingState} */ (
    /** @type {unknown} */ ({ mathFontChecks: 1, unreadyMath: [] })
  );
};
