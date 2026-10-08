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
    timing: globalThis.__mathLoadControl?.timing,
    font_wait: Reflect.get(globalThis, "kpressMathFaceWait") || [],
    font_resources: performance
      .getEntriesByType("resource")
      .filter((entry) => entry.name.endsWith(".woff2"))
      .map((entry) => {
        const resource = /** @type {PerformanceResourceTiming} */ (entry);
        return {
          name: resource.name,
          start: resource.startTime,
          end: resource.responseEnd,
          kind: resource.initiatorType,
          transferred: resource.transferSize,
        };
      }),
  };
};
