// The removed-width control: let the first measured box size to its glyphs, keeping its and
// its base's styles in `__brokenGeometry` for `restore_first_reservation`.
() => {
  const box = /** @type {HTMLElement} */ (
    /** @type {HTMLElement[]} */ (globalThis.__squaresGeometryBoxes)[0]
  );
  globalThis.__brokenGeometry = [
    box,
    box.style.cssText,
    /** @type {HTMLElement} */ (box.firstElementChild).style.cssText,
  ];
  box.style.width = "auto";
  /** @type {HTMLElement} */ (box.firstElementChild).style.position = "relative";
};
