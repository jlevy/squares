// How the current document was reached: `reload` after a real reload.
() =>
  /** @type {PerformanceNavigationTiming} */ (performance.getEntriesByType("navigation")[0]).type;
