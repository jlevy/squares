// What the page's global key handler would have changed if it had acted: capture mode, the
// transport's state, and where the focus and the Search seeds field stand. Read from the DOM
// because `window.atlasTransitions` refuses every read while Search or Pack owns the page.
() => {
  const seeds = /** @type {HTMLInputElement | null} */ (document.getElementById("search-seeds"));
  return {
    capture: document.body.classList.contains("capture"),
    transport: document.getElementById("play")?.getAttribute("aria-label") ?? null,
    focused: document.activeElement?.id ?? null,
    seeds: seeds?.value ?? null,
  };
};
