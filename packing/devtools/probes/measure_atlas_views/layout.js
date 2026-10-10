// The homepage's atlas as laid out now: the view it is in, how many tiles a line holds,
// the box of tiles, every tile that shows with its box, its drawing's box and the size
// of its number, the view tabs with which is selected, in the tab order and focused, the
// panel the tabs control, the query string, how many tiles are in a move, and how far
// the page runs past the window sideways. Boxes are in CSS pixels from the window's top
// left corner, as transformed: a tile in a move is reported where it is drawn. A move is
// an animation the script started; a tile's hover wash, a CSS transition, is not one.
//
// And the size it is at: the size tabs as the view tabs are reported, the key to a tile's
// marks under them, and for each tile its outline and number-ink bounds. Obsolete
// stars and layer badges are reported as null where absent, so regressions are visible.
(/** @type {{pan?: 'start' | 'end'} | undefined} */ options) => {
  /** @param {number} value */
  const round = (value) => Math.round(value * 100) / 100;
  /** @param {Element} element */
  const box = (element) => {
    const rect = element.getBoundingClientRect();
    return {
      left: round(rect.left),
      top: round(rect.top),
      right: round(rect.right),
      bottom: round(rect.bottom),
      width: round(rect.width),
      // Keep height exact: rounding it accumulates error across long triangles.
      height: rect.height,
    };
  };
  const block = document.querySelector("[data-atlas-grid]");
  const cells = block?.querySelector(".site-atlas-cells");
  if (!(block instanceof HTMLElement) || !(cells instanceof HTMLElement)) {
    return null;
  }
  if (options?.pan) {
    cells.scrollLeft = options.pan === "start" ? -cells.scrollWidth : 0;
  }
  const tiles = [...cells.querySelectorAll(".site-atlas-cell")].filter(
    (tile) => tile instanceof HTMLElement && tile.getClientRects().length > 0,
  );
  const rows = [...cells.querySelectorAll(".site-atlas-row")].filter(
    (row) => row.getClientRects().length > 0,
  );
  const cellsStyle = getComputedStyle(cells);
  const rootSize = Number.parseFloat(getComputedStyle(document.documentElement).fontSize);
  const referenceGap = cellsStyle.getPropertyValue("--site-atlas-reference-gap").trim();
  const referenceGapPx =
    Number.parseFloat(referenceGap) * (referenceGap.endsWith("rem") ? rootSize : 1);
  const inkInset = Number.parseFloat(cellsStyle.getPropertyValue("--site-atlas-ink-inset"));
  const inkContext = document.createElement("canvas").getContext("2d");
  /** @param {Element | null} number */
  const numberInk = (number) => {
    if (!number || !inkContext) {
      return null;
    }
    const style = getComputedStyle(number);
    const rect = number.getBoundingClientRect();
    inkContext.font = `${style.fontStyle} ${style.fontWeight} ${style.fontSize} ${style.fontFamily}`;
    const metrics = inkContext.measureText(number.textContent?.trim() ?? "");
    const baseline =
      rect.top +
      (rect.height - metrics.fontBoundingBoxAscent - metrics.fontBoundingBoxDescent) / 2 +
      metrics.fontBoundingBoxAscent;
    return {
      top: baseline - metrics.actualBoundingBoxAscent,
      bottom: baseline + metrics.actualBoundingBoxDescent,
    };
  };
  const first = rows[0];
  const last = rows.at(-1);
  const canvas =
    block.dataset.atlasView === "triangle" && first && last
      ? { ...box(first), bottom: box(last).bottom, height: box(last).bottom - box(first).top }
      : box(cells);
  const moving = document
    .getAnimations()
    .filter(
      (animation) =>
        !(animation instanceof CSSTransition) &&
        animation.effect instanceof KeyframeEffect &&
        animation.effect.target?.matches(".site-atlas-cell") === true &&
        animation.playState !== "finished",
    );
  const toggle = block.querySelector("[data-atlas-toggle]");
  /**
   * @param {Element} tab
   * @param {string | null} key
   */
  const tabReport = (tab, key) => ({
    key,
    id: tab.id,
    label: (tab.textContent ?? "").trim(),
    selected: tab.getAttribute("aria-selected"),
    controls: tab.getAttribute("aria-controls"),
    description: tab.getAttribute("aria-description"),
    tabindex: tab instanceof HTMLElement ? tab.tabIndex : null,
    focused: tab === document.activeElement,
    shown: tab.getClientRects().length > 0,
    box: box(tab),
    font_px: round(Number.parseFloat(getComputedStyle(tab).fontSize)),
  });
  const legend = block.querySelector("[data-atlas-legend]");
  const viewStrip = block.querySelector("[data-atlas-views]");
  return {
    view: block.dataset.atlasView ?? null,
    view_strip: viewStrip ? box(viewStrip) : null,
    size: block.dataset.atlasSize ?? null,
    scale: block.dataset.atlasScale ?? "fixed",
    largest_side: Number.parseFloat(
      getComputedStyle(cells).getPropertyValue("--site-atlas-global-side"),
    ),
    per_line: Math.round(
      (cells.getBoundingClientRect().width + referenceGapPx) /
        ((tiles[0]?.getBoundingClientRect().width ?? 1) + referenceGapPx),
    ),
    cells: box(cells),
    canvas,
    frame: {
      top: cells.getBoundingClientRect().top + cells.clientTop,
      bottom: cells.getBoundingClientRect().top + cells.clientTop + cells.clientHeight,
      client_top: cells.clientTop,
      client_height: cells.clientHeight,
    },
    pan: { left: cells.scrollLeft, width: cells.scrollWidth, viewport: cells.clientWidth },
    line_gap_px: rows[1] ? Number.parseFloat(getComputedStyle(rows[1]).marginBlockStart) : 0,
    gap_px: round(Number.parseFloat(cellsStyle.columnGap)),
    reference_gap_px: referenceGapPx,
    row_gap_px: Number.parseFloat(cellsStyle.rowGap),
    block: box(block),
    panel: {
      id: cells.id,
      role: cells.getAttribute("role"),
      labelledby: cells.getAttribute("aria-labelledby"),
    },
    tabs: [...block.querySelectorAll("[data-atlas-tab]")].map((tab) =>
      tabReport(tab, tab instanceof HTMLElement ? (tab.dataset.atlasTab ?? null) : null),
    ),
    sizes: [...block.querySelectorAll("[data-atlas-size-tab]")].map((tab) =>
      tabReport(tab, tab instanceof HTMLElement ? (tab.dataset.atlasSizeTab ?? null) : null),
    ),
    scales: [...block.querySelectorAll("[data-atlas-scale-tab]")].map((tab) =>
      tabReport(tab, tab instanceof HTMLElement ? (tab.dataset.atlasScaleTab ?? null) : null),
    ),
    legend:
      legend === null
        ? null
        : {
            text: [...legend.querySelectorAll("[data-atlas-legend-key]")]
              .filter((item) => item.getClientRects().length > 0)
              .map((item) => item.textContent ?? "")
              .join(" ")
              .replace(/\s+/g, " ")
              .trim(),
            shown: legend.getClientRects().length > 0,
            box: box(legend),
            font_px: round(Number.parseFloat(getComputedStyle(legend).fontSize)),
            columns: [...legend.querySelectorAll(".site-atlas-legend-column")].map((column) => ({
              box: box(column),
              items: [...column.querySelectorAll("[data-atlas-legend-key]")].map((item) => ({
                key: item.getAttribute("data-atlas-legend-key"),
                text: (item.textContent ?? "").trim(),
                box: box(item),
                swatches: [...item.querySelectorAll(".site-atlas-swatch")].map((swatch) => ({
                  value: swatch.getAttribute("data-value"),
                  label: swatch.textContent?.trim() ?? "",
                  fill: getComputedStyle(swatch).backgroundColor,
                  ink: getComputedStyle(swatch).color,
                  ...box(swatch),
                })),
              })),
            })),
          },
    expanded: toggle?.getAttribute("aria-expanded") ?? null,
    search: location.search,
    hash: location.hash,
    // A tile by its case, else an element by its id, else a link, as the key's is, by its
    // text.
    focus:
      document.activeElement?.getAttribute("data-atlas-n") ??
      (document.activeElement?.id ||
        (document.activeElement instanceof HTMLAnchorElement
          ? document.activeElement.textContent.trim()
          : null)),
    moving: moving.length,
    overflow: document.documentElement.scrollWidth - document.documentElement.clientWidth,
    tiles: tiles.map((tile) => {
      const drawing = tile.querySelector("svg, img");
      const number = tile.querySelector(".site-atlas-n");
      const mark = tile.querySelector(".site-atlas-layer-mark");
      const star = tile.querySelector(".site-star");
      const gridMarker = tile.querySelector(".site-atlas-grid-start");
      return {
        n: Number(tile instanceof HTMLElement ? tile.dataset.atlasN : Number.NaN),
        side: Number(tile.getAttribute("data-atlas-side")),
        drawing_slot_width: drawing ? Number.parseFloat(getComputedStyle(drawing).width) : null,
        grid_from: tile.hasAttribute("data-atlas-grid-from"),
        grid_marker: (gridMarker?.getClientRects().length ?? 0) > 0,
        grid_label: gridMarker
          ? [...gridMarker.children].map((line) => line.textContent.trim()).join(" ")
          : null,
        grid_marker_lines: gridMarker
          ? [...gridMarker.children]
              .filter((line) => line.getClientRects().length > 0)
              .map((line) => ({ text: line.textContent.trim(), ...box(line) }))
          : [],
        grid_marker_box: gridMarker?.getClientRects().length ? box(gridMarker) : null,
        ...box(tile),
        drawing: drawing ? box(drawing) : null,
        outline: drawing
          ? {
              left:
                drawing.getBoundingClientRect().left +
                drawing.getBoundingClientRect().width * inkInset,
              right:
                drawing.getBoundingClientRect().right -
                drawing.getBoundingClientRect().width * inkInset,
              top:
                drawing.getBoundingClientRect().top +
                drawing.getBoundingClientRect().width * inkInset,
              bottom:
                drawing.getBoundingClientRect().bottom -
                drawing.getBoundingClientRect().width * inkInset,
            }
          : null,
        number_px: number ? round(Number.parseFloat(getComputedStyle(number).fontSize)) : null,
        number_width: number ? round(number.scrollWidth) : null,
        name: tile.getAttribute("aria-label"),
        number_box: number ? box(number) : null,
        number_ink: numberInk(number),
        mark: mark ? box(mark) : null,
        star: star ? box(star) : null,
      };
    }),
  };
};
