// Whether focus sits on the visible toggle button for the certificate named by the argument,
// rather than on a control that switching certificates hid.
/** @param {string} slug */
(slug) => {
  const active = /** @type {HTMLElement} */ (document.activeElement);
  return (
    active.matches(".cert-toggle button") &&
    active.dataset.cert === slug &&
    active.getClientRects().length > 0
  );
};
