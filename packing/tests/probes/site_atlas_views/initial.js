// Direct query geometry with the atlas programs withheld: the head bootstrap and
// container stylesheet must put every visible tile inside the phone's atlas box.
() => {
  const cells = document.querySelector(".site-atlas-cells");
  if (!(cells instanceof HTMLElement)) {
    return null;
  }
  const box = cells.getBoundingClientRect();
  const style = getComputedStyle(cells);
  const rows = [...cells.querySelectorAll(".site-atlas-row")].filter(
    (row) => row.getClientRects().length > 0,
  );
  const first = rows[0]?.getBoundingClientRect();
  const last = rows.at(-1)?.getBoundingClientRect();
  const triangle = document.documentElement.dataset.siteAtlasView !== "grid";
  const canvas =
    triangle && first && last
      ? {
          left: first.left - box.left,
          right: first.right - box.left,
          top: first.top - box.top,
          bottom: last.bottom - box.top,
          width: first.width,
          height: last.bottom - first.top,
        }
      : {
          left: 0,
          right: box.width,
          top: 0,
          bottom: box.height,
          width: box.width,
          height: box.height,
        };
  return {
    canvas,
    frame: {
      top: cells.clientTop,
      bottom: cells.clientTop + cells.clientHeight,
      client_top: cells.clientTop,
      client_height: cells.clientHeight,
    },
    line_gap_px: rows[1] ? Number.parseFloat(getComputedStyle(rows[1]).marginBlockStart) : 0,
    page_overflow: document.documentElement.scrollWidth - document.documentElement.clientWidth,
    supported: {
      division: CSS.supports("width", "calc(1px / 1px * 1px)"),
      round: CSS.supports("opacity", "round(down, 1.5, 1)"),
      mod: CSS.supports("opacity", "mod(3, 2)"),
    },
    view: document.documentElement.dataset.siteAtlasView ?? "triangle",
    size: document.documentElement.dataset.siteAtlasSize ?? "small",
    scale: document.documentElement.dataset.siteAtlasScale ?? "fixed",
    largest_side: Number.parseFloat(style.getPropertyValue("--site-atlas-global-side")),
    columns: Math.round(
      (box.width + Number.parseFloat(style.columnGap)) /
        ((cells.querySelector(".site-atlas-cell")?.getBoundingClientRect().width ?? 1) +
          Number.parseFloat(style.columnGap)),
    ),
    width: box.width,
    height: box.height,
    gap_px: Number.parseFloat(style.columnGap),
    overflow: cells.scrollWidth - cells.clientWidth,
    tiles: [...cells.querySelectorAll(".site-atlas-cell")]
      .filter((tile) => tile.getClientRects().length > 0)
      .map((tile) => {
        const at = tile.getBoundingClientRect();
        const drawing = tile.querySelector("img, svg");
        const gridMarker = tile.querySelector(".site-atlas-grid-start");
        return {
          n: Number(tile.getAttribute("data-atlas-n")),
          left: at.left - box.left,
          right: at.right - box.left,
          top: at.top - box.top,
          bottom: at.bottom - box.top,
          width: at.width,
          height: at.height,
          side: Number(tile.getAttribute("data-atlas-side")),
          drawing_slot_width: drawing ? Number.parseFloat(getComputedStyle(drawing).width) : null,
          drawing_width: tile.querySelector("img, svg")?.getBoundingClientRect().width,
          grid_from: tile.hasAttribute("data-atlas-grid-from"),
          grid_marker:
            (tile.querySelector(".site-atlas-grid-start")?.getClientRects().length ?? 0) > 0,
          grid_label: gridMarker
            ? [...gridMarker.children].map((line) => line.textContent.trim()).join(" ")
            : null,
          grid_marker_lines: gridMarker
            ? [...gridMarker.children]
                .filter((line) => line.getClientRects().length > 0)
                .map((line) => ({
                  text: line.textContent.trim(),
                  top: line.getBoundingClientRect().top,
                }))
            : [],
        };
      }),
  };
};
