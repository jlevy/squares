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
    /** @type {{startTime: number, durationMs: number, name: string}[]} */
    longTasks: [],
    /** @type {{startTime: number, durationMs: number}[]} */
    readabilitySamples: [],
    /** @type {{startTime: number, durationMs: number, renderStart: number, styleAndLayoutStart: number, scripts: {executionStart: number, durationMs: number, forcedStyleAndLayoutDurationMs: number, sourceURL: string, sourceFunctionName: string, invoker: string}[]}[]} */
    animationFrames: [],
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
      // Retain bounded diagnostic timing; every task still contributes to the guards.
      if (state.longTasks.length < 100) {
        state.longTasks.push({
          startTime: entry.startTime,
          durationMs: entry.duration,
          name: entry.name,
        });
      }
    }
  }).observe({ type: "longtask", buffered: true });
  // Optional native attribution supplements the long-task timeline; it never
  // replaces that metric or exempts any task from the existing limits.
  if (supported.includes("long-animation-frame")) {
    new PerformanceObserver((list) => {
      for (const entry of list.getEntries()) {
        if (state.animationFrames.length >= 30) {
          break;
        }
        const frame =
          /** @type {PerformanceEntry & {renderStart: number, styleAndLayoutStart: number, scripts: {executionStart: number, duration: number, forcedStyleAndLayoutDuration: number, sourceURL: string, sourceFunctionName: string, invoker: string}[]}} */ (
            entry
          );
        state.animationFrames.push({
          startTime: frame.startTime,
          durationMs: frame.duration,
          renderStart: frame.renderStart,
          styleAndLayoutStart: frame.styleAndLayoutStart,
          scripts: frame.scripts.slice(0, 8).map((script) => ({
            executionStart: script.executionStart,
            durationMs: script.duration,
            forcedStyleAndLayoutDurationMs: script.forcedStyleAndLayoutDuration,
            sourceURL: script.sourceURL,
            sourceFunctionName: script.sourceFunctionName,
            invoker: script.invoker,
          })),
        });
      }
    }).observe({ type: "long-animation-frame", buffered: true });
  }
};
