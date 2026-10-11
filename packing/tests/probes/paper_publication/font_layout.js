// Attribute cold paper-front shifts to their actual nodes and font arrival times.
() => {
  const root =
    /** @type {typeof globalThis & {paperFontLayout?: {shifts: Record<string, unknown>[], fonts: Record<string, unknown>[]}}} */ (
      globalThis
    );
  if (root.paperFontLayout) {
    return {
      ...root.paperFontLayout,
      resources: performance
        .getEntriesByType("resource")
        .filter((entry) => /\.(?:woff2|css)$/.test(entry.name))
        .map((entry) => {
          const resource = /** @type {PerformanceResourceTiming} */ (entry);
          return {
            name: resource.name,
            start: resource.startTime,
            end: resource.responseEnd,
            kind: resource.initiatorType,
          };
        }),
    };
  }
  /** @type {{shifts: Record<string, unknown>[], fonts: Record<string, unknown>[]}} */
  const state = { shifts: [], fonts: [] };
  root.paperFontLayout = state;
  new PerformanceObserver((list) => {
    for (const entry of list.getEntries()) {
      const shift =
        /** @type {PerformanceEntry & {value: number, hadRecentInput: boolean, sources?: {node?: Node, previousRect: DOMRectReadOnly, currentRect: DOMRectReadOnly}[]}} */ (
          entry
        );
      if (!shift.hadRecentInput) {
        state.shifts.push({
          at: shift.startTime,
          value: shift.value,
          sources: (shift.sources ?? []).map((source) => ({
            node:
              source.node instanceof Element
                ? `${source.node.tagName}.${source.node.className}`
                : source.node?.nodeName,
            text: source.node?.textContent?.slice(0, 100),
            before: source.previousRect.toJSON(),
            after: source.currentRect.toJSON(),
          })),
        });
      }
    }
  }).observe({ type: "layout-shift", buffered: true });
  document.fonts.addEventListener("loadingdone", () => {
    state.fonts.push({
      at: performance.now(),
      loaded: [...document.fonts]
        .filter((face) => face.status === "loaded")
        .map((face) => `${face.family} ${face.weight}`),
    });
  });
  return state;
};
