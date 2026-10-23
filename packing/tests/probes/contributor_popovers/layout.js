() => {
  const table = document.querySelector(".site-profile-table");
  const directory =
    table instanceof HTMLTableElement
      ? {
          headers: Array.from(table.tHead?.rows[0]?.cells ?? [], (cell) =>
            cell.textContent?.trim(),
          ),
          rows: Array.from(table.tBodies[0]?.rows ?? [], (row) => ({
            name: row.cells[0]?.textContent?.trim(),
            keys: Array.from(
              row.cells,
              (cell) => cell.getAttribute("data-value") ?? cell.textContent?.trim() ?? "",
            ),
          })),
          tallies: Array.from(table.querySelectorAll(".site-credit-tally")).flatMap((tally) => {
            const total = tally.querySelector(":scope > a");
            const levels = tally.querySelector(":scope > .site-tally-levels");
            if (!total || !levels) {
              return [];
            }
            return [
              {
                column: tally.closest("td")?.className,
                totalBottom: total.getBoundingClientRect().bottom,
                levelsTop: levels.getBoundingClientRect().top,
                totalColor: getComputedStyle(total).color,
                tallyColor: getComputedStyle(tally).color,
                levelsColor: getComputedStyle(levels).color,
                levelLinkColors: Array.from(
                  levels.querySelectorAll("a"),
                  (link) => getComputedStyle(link).color,
                ),
              },
            ];
          }),
        }
      : null;
  return { directory };
};
