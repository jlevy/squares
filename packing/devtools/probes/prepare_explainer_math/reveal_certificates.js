// Unhide every certificate figure: hidden certificate copies need their own measured context.
() => {
  for (const el of /** @type {NodeListOf<HTMLElement>} */ (
    document.querySelectorAll(".cert-figure")
  )) {
    el.hidden = false;
  }
};
