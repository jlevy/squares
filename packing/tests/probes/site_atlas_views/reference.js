// Row's decorative reference frame as the browser paints it. A pseudo-element
// has no DOMRect, so its used offsets and border-box dimensions locate its outline.
() => {
  const cells = document.querySelector(".site-atlas-cells");
  if (!(cells instanceof HTMLElement)) {
    return null;
  }
  const wanted = new Set([1, 2, 3, 4, 5, 6, 9, 11, 12, 16, 18, 25, 36, 100]);
  return {
    scale: document.documentElement.dataset.siteAtlasScale ?? "fixed",
    frame: {
      inset: Number.parseFloat(
        getComputedStyle(cells).getPropertyValue("--site-atlas-frame-inset"),
      ),
      span: Number.parseFloat(getComputedStyle(cells).getPropertyValue("--site-atlas-frame-span")),
    },
    tiles: [...cells.querySelectorAll(".site-atlas-cell")]
      .filter((tile) => wanted.has(Number(tile.getAttribute("data-atlas-n"))))
      .map((tile) => {
        const box = tile.getBoundingClientRect();
        const drawing = tile.querySelector("img");
        const image = drawing?.getBoundingClientRect();
        const style = getComputedStyle(tile, "::before");
        const shown = style.content !== "none" && style.display !== "none";
        const width = Number.parseFloat(style.width);
        const height = Number.parseFloat(style.height);
        return {
          n: Number(tile.getAttribute("data-atlas-n")),
          smaller: tile.hasAttribute("data-atlas-row-smaller"),
          padding: Number.parseFloat(getComputedStyle(tile).paddingTop),
          slot_width: drawing ? Number.parseFloat(getComputedStyle(drawing).width) : null,
          tile: { left: box.left, top: box.top, width: box.width, height: box.height },
          drawing: image
            ? { left: image.left, top: image.top, width: image.width, height: image.height }
            : null,
          reference: shown
            ? {
                left: box.left + Number.parseFloat(style.left),
                top: box.top + Number.parseFloat(style.top),
                width,
                height,
                border_width: Number.parseFloat(style.borderTopWidth),
                border_style: style.borderTopStyle,
                ink: style.borderTopColor,
                fill: style.backgroundColor,
                pointer_events: style.pointerEvents,
                box_sizing: style.boxSizing,
              }
            : null,
        };
      }),
  };
};
