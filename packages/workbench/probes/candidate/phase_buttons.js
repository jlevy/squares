// The motion modes the buttons offer, in the order they are laid out.
() =>
  Array.from(
    /** @type {NodeListOf<HTMLButtonElement>} */ (document.querySelectorAll("#phase-seg button")),
  ).map((b) => b.dataset.phase);
