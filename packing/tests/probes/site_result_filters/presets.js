// A table of results under its filter bar, as a link that presets it leaves it: the rows
// showing, the count's words, and each preset-only control (`data-preset`) with the
// facet it filters, its value, the words of the choice it shows and of its label, and
// whether its label is out of the bar.
// Null where the page has no such bar and table.
() => {
  const bar = document.querySelector(".site-result-filters");
  const table = bar?.parentElement?.querySelector(":scope > .site-table-wrap table");
  if (!(bar instanceof HTMLElement) || !(table instanceof HTMLTableElement)) {
    return null;
  }
  const rows = [...(table.tBodies[0]?.rows ?? [])];
  /** @param {HTMLTableRowElement} row */
  const name = (row) => row.id || (row.dataset.result ?? "");
  return {
    page: location.pathname.split("/").at(-1) ?? "",
    search: location.search,
    count: (bar.querySelector(".site-count")?.textContent ?? "").trim(),
    total: rows.length,
    shown: rows.filter((row) => !row.hidden).map(name),
    presets: [...bar.querySelectorAll("select[data-preset]")].flatMap((control) => {
      const label = control.closest("label");
      if (!(control instanceof HTMLSelectElement) || !(label instanceof HTMLElement)) {
        return [];
      }
      const words = [...label.childNodes]
        .filter((node) => node.nodeType === Node.TEXT_NODE)
        .map((node) => (node.textContent ?? "").trim())
        .join(" ")
        .trim();
      return [
        {
          filter: control.getAttribute("data-filter") ?? "",
          value: control.value,
          choice: (control.selectedOptions[0]?.textContent ?? "").trim(),
          label: words,
          out: label.hidden || label.getClientRects().length === 0,
        },
      ];
    }),
  };
};
