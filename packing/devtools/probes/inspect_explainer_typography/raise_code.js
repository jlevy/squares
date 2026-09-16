// The self-test's raised inline code: the element lifted 2px off its baseline.
/** @param {HTMLElement} el */
(el) => {
  el.style.position = "relative";
  el.style.top = "-2px";
};
