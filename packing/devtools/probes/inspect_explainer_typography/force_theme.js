// Forces the screen theme the reader's toggle would: on the root, and on every scope kpress
// has already resolved a theme for.
/** @param {string} theme */
(theme) => {
  document.documentElement.dataset.kpressTheme = theme;
  const scopes = /** @type {NodeListOf<HTMLElement>} */ (
    document.querySelectorAll("[data-kpress-resolved-theme]")
  );
  for (const el of scopes) {
    el.dataset.kpressResolvedTheme = theme;
  }
};
