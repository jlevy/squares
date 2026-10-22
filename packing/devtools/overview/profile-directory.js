// Native profile anchors remain usable with scripts disabled. Fill the rest of a
// directory row's hit area without changing its table semantics or keyboard stops.
(() => {
  const selector = ".site-profile-table tbody tr";
  for (const row of document.querySelectorAll(selector)) {
    row.setAttribute("data-profile-ready", "");
  }
  document.addEventListener("click", (event) => {
    if (
      event.defaultPrevented ||
      event.button !== 0 ||
      event.altKey ||
      event.ctrlKey ||
      event.metaKey ||
      event.shiftKey ||
      !(event.target instanceof Element) ||
      event.target.closest("a, button, input, select, textarea, summary, label") ||
      window.getSelection()?.toString()
    ) {
      return;
    }
    const row = event.target.closest(selector);
    const link = row?.querySelector("td:first-child a[href]");
    if (link instanceof HTMLAnchorElement) {
      window.location.assign(link.href);
    }
  });
})();
