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
    columns: style.gridTemplateColumns.split(/\s+/).length,
    width: box.width,
    overflow: cells.scrollWidth - cells.clientWidth,
    tiles: [...cells.querySelectorAll(".site-atlas-cell")]
      .filter((tile) => tile.getClientRects().length > 0)
      .map((tile) => {
        const at = tile.getBoundingClientRect();
        return {
          n: Number(tile.getAttribute("data-atlas-n")),
          left: at.left - box.left,
          right: at.right - box.left,
          top: at.top - box.top,
          width: at.width,
        };
      }),
  };
};
