// Measure the SVG reference's centered stroke in the same coordinates as the packing.
() => {
  const cells = document.querySelector(".site-atlas-cells");
  if (!(cells instanceof HTMLElement)) {
    return null;
  }
  const wanted = new Set([1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 12, 16, 18, 19, 25, 36, 100]);
  return {
    scale:
      document.documentElement.dataset.siteAtlasScale ??
      cells.closest("[data-atlas-grid]")?.getAttribute("data-atlas-scale") ??
      "row",
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
        const reference = tile.querySelector(".site-atlas-reference");
        const rect = reference?.querySelector("rect");
        const shown =
          reference instanceof SVGSVGElement &&
          rect instanceof SVGRectElement &&
          getComputedStyle(reference).display !== "none";
        const outline = shown ? rect.getBoundingClientRect() : null;
        const style = shown ? getComputedStyle(rect) : null;
        return {
          n: Number(tile.getAttribute("data-atlas-n")),
          smaller: tile.hasAttribute("data-atlas-row-smaller"),
          padding: Number.parseFloat(getComputedStyle(tile).paddingTop),
          slot_width: drawing ? Number.parseFloat(getComputedStyle(drawing).width) : null,
          tile: { left: box.left, top: box.top, width: box.width, height: box.height },
          drawing: image
            ? {
                left: image.left,
                top: image.top,
                width: image.width,
                height: image.height,
                z_index: drawing ? getComputedStyle(drawing).zIndex : null,
              }
            : null,
          reference:
            shown && outline && style
              ? {
                  left: outline.left,
                  top: outline.top,
                  width: outline.width,
                  height: outline.height,
                  stroke_width:
                    (Number.parseFloat(style.strokeWidth) *
                      reference.getBoundingClientRect().width) /
                    reference.viewBox.baseVal.width,
                  ink: style.stroke,
                  fill: style.fill,
                  pointer_events: getComputedStyle(reference).pointerEvents,
                  z_index: getComputedStyle(reference).zIndex,
                }
              : null,
        };
      }),
  };
};
