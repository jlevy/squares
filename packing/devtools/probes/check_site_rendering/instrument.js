// Start before navigation. Observers record native timing without polling layout.
() => {
  const supported = PerformanceObserver.supportedEntryTypes;
  const state = {
    supported: ["layout-shift", "largest-contentful-paint", "longtask"].every((type) =>
      supported.includes(type),
    ),
    cls: 0,
    windowValue: 0,
    windowStart: 0,
    lastShift: 0,
    lcpMs: 0,
    longestTaskMs: 0,
    blockingMs: 0,
    shifts: 0,
  };
  Object.assign(window, { siteRenderingMeasure: state });
  if (!state.supported) {
    return;
  }
  new PerformanceObserver((list) => {
    for (const entry of list.getEntries()) {
      const shift = /** @type {PerformanceEntry & {value: number, hadRecentInput: boolean}} */ (
        entry
      );
      if (shift.hadRecentInput) {
        continue;
      }
      if (shift.startTime - state.lastShift > 1000 || shift.startTime - state.windowStart > 5000) {
        state.windowValue = 0;
        state.windowStart = shift.startTime;
      }
      state.windowValue += shift.value;
      state.cls = Math.max(state.cls, state.windowValue);
      state.lastShift = shift.startTime;
      state.shifts += 1;
    }
  }).observe({ type: "layout-shift", buffered: true });
  new PerformanceObserver((list) => {
    for (const entry of list.getEntries()) {
      state.lcpMs = Math.max(state.lcpMs, entry.startTime);
    }
  }).observe({ type: "largest-contentful-paint", buffered: true });
  new PerformanceObserver((list) => {
    for (const entry of list.getEntries()) {
      state.longestTaskMs = Math.max(state.longestTaskMs, entry.duration);
      state.blockingMs += Math.max(0, entry.duration - 50);
    }
  }).observe({ type: "longtask", buffered: true });
};
