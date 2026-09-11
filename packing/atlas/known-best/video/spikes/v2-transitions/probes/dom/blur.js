// Take the focus off whatever holds it.
() => {
  if (document.activeElement) {
    /** @type {HTMLElement | SVGElement} */ (document.activeElement).blur();
  }
};
