// Removes the crop markers `math_contexts.js` and `code_contexts.js` placed, so the next
// medium's pass marks its own blocks rather than finding the last one's.
() => {
  /** @type {NodeListOf<HTMLElement>} */ (
    document.querySelectorAll("[data-squares-typography-crop]")
  ).forEach((el) => {
    delete el.dataset.squaresTypographyCrop;
  });
  /** @type {NodeListOf<HTMLElement>} */ (
    document.querySelectorAll("[data-squares-code-crop]")
  ).forEach((el) => {
    delete el.dataset.squaresCodeCrop;
  });
};
