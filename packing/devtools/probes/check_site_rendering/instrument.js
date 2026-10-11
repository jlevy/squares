// Start before navigation. Observers record native timing without polling layout.
() => {
  /** @typedef {{x: number, y: number, width: number, height: number}} ShiftRect */
  /** @typedef {{node: Node | null, previousRect: DOMRectReadOnly, currentRect: DOMRectReadOnly}} ShiftSource */
  /** @param {Node | null} node */
  const identify = (node) => {
    if (!node) {
      return null;
    }
    const sourceElement = node instanceof Element ? node : node.parentElement;
    if (!sourceElement) {
      return null;
    }
    const parts = node instanceof Element ? [] : [node.nodeName];
    /** @type {Element | null} */
    let element = sourceElement;
    for (let depth = 0; element && depth < 3; depth += 1) {
      const id = element.id.slice(0, 120);
      const classes = (element.getAttribute("class") ?? "").trim().slice(0, 120);
      parts.unshift(
        `${element.localName}${id ? `#${id}` : ""}${classes ? `.${classes.split(/\s+/).slice(0, 3).join(".")}` : ""}`,
      );
      element = element.parentElement;
    }
    return parts.join(" > ").slice(-512);
  };
  /** @param {DOMRectReadOnly} rect @returns {ShiftRect} */
  const rectangle = (rect) => ({ x: rect.x, y: rect.y, width: rect.width, height: rect.height });
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
    /** @type {{startTime: number, value: number, sources: {node: string | null, previousRect: ShiftRect, currentRect: ShiftRect}[]}[]} */
    layoutShifts: [],
    /** @type {{startTime: number, type: string}[]} */
    fontEvents: [],
    /** @type {{startTime: number, durationMs: number, name: string}[]} */
    longTasks: [],
    /** @type {{startTime: number, durationMs: number}[]} */
    readabilitySamples: [],
    /** @type {{startTime: number, durationMs: number, renderStart: number, styleAndLayoutStart: number, scripts: {executionStart: number, durationMs: number, forcedStyleAndLayoutDurationMs: number, sourceURL: string, sourceFunctionName: string, invoker: string}[]}[]} */
    animationFrames: [],
  };
  Object.assign(window, { siteRenderingMeasure: state });
  // Native font events place face arrival on the same clock as layout shifts.
  /** @param {Event} event */
  const recordFontEvent = (event) => {
    if (state.fontEvents.length < 100) {
      state.fontEvents.push({ startTime: event.timeStamp, type: event.type });
    }
  };
  document.fonts.addEventListener("loading", recordFontEvent);
  document.fonts.addEventListener("loadingdone", recordFontEvent);
  if (!state.supported) {
    return;
  }
  new PerformanceObserver((list) => {
    for (const entry of list.getEntries()) {
      const shift =
        /** @type {PerformanceEntry & {value: number, hadRecentInput: boolean, sources: ShiftSource[]}} */ (
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
      // Bound diagnostics only. All shifts still contribute to the unchanged CLS guard.
      // Rectangles come from the native entry, never from a fresh layout read.
      if (state.layoutShifts.length < 100) {
        state.layoutShifts.push({
          startTime: shift.startTime,
          value: shift.value,
          sources: shift.sources.slice(0, 5).map((source) => ({
            node: identify(source.node),
            previousRect: rectangle(source.previousRect),
            currentRect: rectangle(source.currentRect),
          })),
        });
      }
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
