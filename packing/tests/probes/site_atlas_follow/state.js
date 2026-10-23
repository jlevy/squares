// One reading of a following triangle: its attributes, its zoom and pan, the focus line
// and where it falls, and how the reader's row is framed. Lengths are as drawn.
() => {
  const block = document.querySelector("[data-atlas-grid]");
  const cells = block?.querySelector(".site-atlas-cells");
  if (!(block instanceof HTMLElement) || !(cells instanceof HTMLElement)) {
    return null;
  }
  const rows = [...cells.querySelectorAll(".site-atlas-row")].filter(
    (row) => row instanceof HTMLElement && row.closest("[hidden]") === null,
  );
  const first = rows[0];
  const drawn =
    first instanceof HTMLElement ? /scale\(([\d.]+)\)/.exec(first.style.transform) : null;
  const scale = drawn ? Number(drawn[1]) : 1;
  const box = cells.getBoundingClientRect();
  const line = SiteAtlasView.focusLine(
    window.innerHeight,
    box.top + window.scrollY,
    window.scrollY,
  );
  /** @param {Element} row */
  const ends = (row) => {
    const boxes = [...row.querySelectorAll(".site-atlas-segment")]
      .map((segment) => segment.getBoundingClientRect())
      .filter((segment) => segment.width > 0);
    return {
      top: row.getBoundingClientRect().top,
      left: Math.min(...boxes.map((segment) => segment.left)),
      right: Math.max(...boxes.map((segment) => segment.right)),
    };
  };
  const read = rows.map(ends);
  const at = SiteAtlasView.along(
    read.map((row) => row.top),
    line,
  );
  const here = read[at.index];
  const next = read[at.index + 1] ?? here;
  const left = here && next ? SiteAtlasView.between(here.left, next.left, at.through) : box.left;
  const right =
    here && next ? SiteAtlasView.between(here.right, next.right, at.through) : box.right;
  const middle = box.left + cells.clientWidth / 2;
  const tab = block.querySelector('[data-atlas-size-tab][aria-selected="true"]');
  const tile = cells.querySelector(".site-atlas-cell");
  const number = cells.querySelector(".site-atlas-n");
  const header = document.querySelector(".site-headroom");
  return {
    follow: block.dataset.atlasFollow ?? null,
    armed: document.documentElement.hasAttribute("data-site-atlas-follow"),
    zoomed: block.hasAttribute("data-atlas-zoom"),
    view: block.dataset.atlasView ?? null,
    size: block.dataset.atlasSize ?? null,
    explicit: block.hasAttribute("data-atlas-size-explicit"),
    shown: tab instanceof HTMLElement ? (tab.dataset.atlasSizeTab ?? null) : null,
    scale,
    pan: cells.scrollLeft,
    scrollY: window.scrollY,
    tile: tile instanceof HTMLElement ? tile.getBoundingClientRect().width : 0,
    number:
      number instanceof HTMLElement
        ? Number.parseFloat(getComputedStyle(number).fontSize) * scale
        : 0,
    line,
    point: (line - box.top) / scale,
    leftEnd: (left - box.left) / cells.clientWidth,
    across: right > left ? (middle - left) / (right - left) : 0,
    headerHidden:
      header instanceof HTMLElement && header.classList.contains("site-headroom-hidden"),
    moving: document
      .getAnimations()
      .filter(
        (animation) =>
          animation.effect instanceof KeyframeEffect &&
          animation.effect.target?.matches(".site-atlas-cell, .site-atlas-cells") === true &&
          animation.playState !== "finished",
      ).length,
  };
};
