// The `disabled` property of the element with this id.
(o) =>
  /** @type {HTMLButtonElement | HTMLInputElement | HTMLSelectElement} */ (
    document.getElementById(o.id)
  ).disabled;
