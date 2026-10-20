// Whether a rating explanation opened since `watch`: a flash shown and removed between
// two reads still counts, which a look at the page afterwards would miss.
(/** @type {{ watch?: boolean } | null} */ options) => {
  const root = document.documentElement;
  if (options?.watch) {
    delete root.dataset.probeTooltipOpened;
    new MutationObserver((records, observer) => {
      for (const record of records) {
        for (const node of record.addedNodes) {
          if (node instanceof HTMLElement && node.classList.contains("site-rating-tooltip")) {
            root.dataset.probeTooltipOpened = "true";
            observer.disconnect();
          }
        }
      }
    }).observe(document.body, { childList: true, subtree: true });
    return null;
  }
  return root.dataset.probeTooltipOpened === "true";
};
