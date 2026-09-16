// Undo `break_first_reservation`: restore the box's and its base's styles.
() => {
  const [box, style, childStyle] = /** @type {[HTMLElement, string, string]} */ (
    globalThis.__brokenGeometry
  );
  box.style.cssText = style;
  /** @type {HTMLElement} */ (box.firstElementChild).style.cssText = childStyle;
};
