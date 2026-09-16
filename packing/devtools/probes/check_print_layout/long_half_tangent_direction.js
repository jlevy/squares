// Moves the direction slider to 118, or to its maximum where that is lower, without the
// event a person's input would send.
/** @param {HTMLInputElement} el */
(el) => {
  el.value = String(Math.min(118, Number(el.max)));
};
