// The homepage's atlas as laid out now: the view it is in, how many tiles a line holds,
// the box of tiles, every tile that shows with its box, its drawing's box and the size
// of its number, the view tabs with which is selected, in the tab order and focused, the
// panel the tabs control, the query string, how many tiles are in a move, and how far
// the page runs past the window sideways. Boxes are in CSS pixels from the window's top
// left corner, as transformed: a tile in a move is reported where it is drawn. A move is
// an animation the script started; a tile's hover wash, a CSS transition, is not one.
//
// And the drawing it is in: the drawing tabs as the view tabs are reported, the cases
// that have a regularized drawing (the third template's), and for each tile which
// drawing it carries, its number's box and its badge's box, `null` where it has none.
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
  const drawings = block.querySelector("template[data-atlas-regularized]");
  return {
    view: block.dataset.atlasView ?? null,
    layer: block.dataset.atlasLayer ?? null,
    regularized:
      drawings instanceof HTMLTemplateElement
        ? [...drawings.content.querySelectorAll(".site-atlas-cell")].map((tile) =>
            Number(tile instanceof HTMLElement ? tile.dataset.atlasN : Number.NaN),
          )
        : [],
    per_line: Number(cells.style.getPropertyValue("--site-atlas-per-line")) || null,
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
    layers: [...block.querySelectorAll("[data-atlas-layer-tab]")].map((tab) =>
      tabReport(tab, tab instanceof HTMLElement ? (tab.dataset.atlasLayerTab ?? null) : null),
    ),
    expanded: toggle?.getAttribute("aria-expanded") ?? null,
    search: location.search,
    hash: location.hash,
    focus:
      document.activeElement?.getAttribute("data-atlas-n") ?? document.activeElement?.id ?? null,
    moving: moving.length,
    overflow: document.documentElement.scrollWidth - document.documentElement.clientWidth,
    tiles: tiles.map((tile) => {
      const drawing = tile.querySelector("svg");
      const number = tile.querySelector(".site-atlas-n");
      const mark = tile.querySelector(".site-atlas-layer-mark");
      return {
        n: Number(tile instanceof HTMLElement ? tile.dataset.atlasN : Number.NaN),
        ...box(tile),
        drawing: drawing ? box(drawing) : null,
        number_px: number ? round(Number.parseFloat(getComputedStyle(number).fontSize)) : null,
        number_width: number ? round(number.scrollWidth) : null,
        layer: (tile instanceof HTMLElement ? tile.dataset.atlasLayer : undefined) ?? "house",
        number_box: number ? box(number) : null,
        mark: mark ? box(mark) : null,
      };
    }),
  };
};
