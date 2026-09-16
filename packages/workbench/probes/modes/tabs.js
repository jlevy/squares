// The sub-panel's mode tabs, as [the mode it names, its label, whether it is pressed].
() =>
  Array.from(
    /** @type {NodeListOf<HTMLButtonElement>} */ (document.querySelectorAll("#mode-tabs button")),
  ).map((b) => [b.dataset.mode, b.textContent.trim(), b.getAttribute("aria-pressed")]);
