// Every face the page loaded, as [family, status, unicode range, size adjustment].
() =>
  Array.from(document.fonts).map((f) => [
    f.family.replace(/"/g, ""),
    f.status,
    f.unicodeRange,
    f.sizeAdjust,
  ]);
