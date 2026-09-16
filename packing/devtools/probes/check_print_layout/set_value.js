// Sets a control's value without the event a person's input would send; the caller
// dispatches `input` itself when the figure should hear about it.
/**
 * @param {HTMLInputElement} el
 * @param {string} value
 */
(el, value) => {
  el.value = value;
};
