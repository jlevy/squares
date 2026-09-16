// Stops the frame sampler and returns what `hold_fonts` and `first_paint` observed, in the
// shape of `check_math_loading.LoadingReport`; Python fills in the rest.
() => {
  const state = /** @type {SquaresMathLoadingState} */ (globalThis.__mathLoadingState);
  state.stop = true;
  return {
    held_loads: /** @type {SquaresMathLoadControl} */ (globalThis.__mathLoadControl).heldLoads,
    sliders: 0,
    early_targets: [],
    frames: state.frames,
    math_font_checks: state.mathFontChecks,
    first_paint: globalThis.__mathFirstPaint,
    unready_math: state.unreadyMath,
    early_math: state.earlyMath,
    fallback: state.fallback,
    readouts: [],
    no_javascript: {},
    findings: [],
  };
};
