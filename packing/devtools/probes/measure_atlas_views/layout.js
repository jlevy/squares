// The homepage's atlas as laid out now: the view it is in, how many tiles a line holds,
// the box of tiles, every tile that shows with its box, its drawing's box and the size
// of its number, the view tabs with which is selected, in the tab order and focused, the
// panel the tabs control, the query string, how many tiles are in a move, and how far
// the page runs past the window sideways. Boxes are in CSS pixels from the window's top
// left corner, as transformed: a tile in a move is reported where it is drawn. A move is
// an animation the script started; a tile's hover wash, a CSS transition, is not one.
//
// And the size it is at: the size tabs as the view tabs are reported, the key to a tile's
// marks under them, and for each tile its number's box and the boxes of the marks it
// carries, the new-result star and the regularized drawing's badge, each `null` where
// the tile has none.
() => {
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
      height: round(rect.height),
    };
  };
  const block = document.querySelector("[data-atlas-grid]");
  const cells = block?.querySelector(".site-atlas-cells");
  if (!(block instanceof HTMLElement) || !(cells instanceof HTMLElement)) {
    return null;
  }
  const tiles = [...cells.querySelectorAll(".site-atlas-cell")].filter(
    (tile) => tile instanceof HTMLElement && tile.getClientRects().length > 0,
  );
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
    tabindex: tab instanceof HTMLElement ? tab.tabIndex : null,
    focused: tab === document.activeElement,
    shown: tab.getClientRects().length > 0,
    box: box(tab),
    font_px: round(Number.parseFloat(getComputedStyle(tab).fontSize)),
  });
  const legend = block.querySelector("[data-atlas-legend]");
  return {
    view: block.dataset.atlasView ?? null,
    size: block.dataset.atlasSize ?? null,
    per_line: getComputedStyle(cells).gridTemplateColumns.split(/\s+/).length,
    cells: box(cells),
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
    legend:
      legend === null
        ? null
        : {
            text: (legend.textContent ?? "").replace(/\s+/g, " ").trim(),
            shown: legend.getClientRects().length > 0,
            box: box(legend),
            font_px: round(Number.parseFloat(getComputedStyle(legend).fontSize)),
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
      return {
        n: Number(tile instanceof HTMLElement ? tile.dataset.atlasN : Number.NaN),
        ...box(tile),
        drawing: drawing ? box(drawing) : null,
        number_px: number ? round(Number.parseFloat(getComputedStyle(number).fontSize)) : null,
        number_width: number ? round(number.scrollWidth) : null,
        name: tile.getAttribute("aria-label"),
        number_box: number ? box(number) : null,
        mark: mark ? box(mark) : null,
        star: star ? box(star) : null,
      };
    }),
  };
};
