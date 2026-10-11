// Every shared font file the page fetched, and what started the request: `link` is a
// preload hint, `css` a face the layout discovered only when it set text in it.
() =>
  performance
    .getEntriesByType("resource")
    .filter((entry) => /\/assets\/fonts\/[^/]+\.woff2$/.test(entry.name))
    .map((entry) => ({
      file: entry.name.slice(entry.name.lastIndexOf("/") + 1),
      initiator: /** @type {PerformanceResourceTiming} */ (entry).initiatorType,
    }));
