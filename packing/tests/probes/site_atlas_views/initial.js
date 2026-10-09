// Direct query geometry with the atlas programs withheld: the head bootstrap and
// container stylesheet must put every visible tile inside the phone's atlas box.
() => {
  const cells = document.querySelector(".site-atlas-cells");
  if (!(cells instanceof HTMLElement)) {
    return null;
  }
  const box = cells.getBoundingClientRect();
  const style = getComputedStyle(cells);
  return {
    supported: {
      division: CSS.supports("width", "calc(1px / 1px * 1px)"),
      round: CSS.supports("opacity", "round(down, 1.5, 1)"),
      mod: CSS.supports("opacity", "mod(3, 2)"),
    },
    view: document.documentElement.dataset.siteAtlasView,
    size: document.documentElement.dataset.siteAtlasSize ?? "medium",
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
        const gridMarker = tile.querySelector(".site-atlas-grid-start");
        return {
          n: Number(tile.getAttribute("data-atlas-n")),
          left: at.left - box.left,
          right: at.right - box.left,
          top: at.top - box.top,
          bottom: at.bottom - box.top,
          width: at.width,
          height: at.height,
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
