// Whether certificate visibility, the toggle buttons' pressed state and the URL all agree
// that the certificate named by the argument is the selected one.
/** @param {string} slug */
(slug) =>
  [.../** @type {NodeListOf<HTMLElement>} */ (document.querySelectorAll(".cert-figure"))].every(
    (el) => el.hidden === (el.dataset.cert !== slug),
  ) &&
  [
    .../** @type {NodeListOf<HTMLElement>} */ (document.querySelectorAll(".cert-toggle button")),
  ].every((el) => el.getAttribute("aria-pressed") === String(el.dataset.cert === slug)) &&
  location.hash === `#${slug}`;
