// The actual homepage table: included/visible rows, ordinary record links and the
// complete-table destination. No filter bar or extra hidden rows may appear here.
async () => {
  await document.fonts.ready;
  const table = document.querySelector("table.site-results");
  const scope = document.querySelector(".site-recent-scope");
  const link = document.querySelector("a[data-all-results]");
  if (!(table instanceof HTMLTableElement) || !(link instanceof HTMLAnchorElement)) {
    return null;
  }
  const rows = [...(table.tBodies[0]?.rows ?? [])];
  /** @param {HTMLTableRowElement} row */
  const name = (row) => row.dataset.result ?? row.id;
  return {
    bar_count: document.querySelectorAll(".site-result-filters").length,
    controls: document.querySelectorAll(".site-result-filters [data-filter]").length,
    scope_present: scope !== null,
    included: rows.map(name),
    visible: rows
      .filter((row) => getComputedStyle(row).display !== "none" && row.getClientRects().length > 0)
      .map(name),
    hidden: rows.filter((row) => row.hidden).map(name),
    links: rows.map((row) => ({
      result: name(row),
      href: row.querySelector("a.site-row-open")?.getAttribute("href") ?? "",
    })),
    destination: link.href,
    registered: (link.getAttribute("data-result-ids") ?? "").split(/\s+/),
    retired: JSON.parse(link.getAttribute("data-retired-results") ?? "{}"),
    overflow: document.documentElement.scrollWidth - document.documentElement.clientWidth,
  };
};
