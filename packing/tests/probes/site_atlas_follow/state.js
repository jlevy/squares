// One reading of a following triangle: its attributes, the script's own reading of its
// zoom, pan and journey, and how the drawn rows are framed. Lengths are as drawn.
() => {
  const block = document.querySelector("[data-atlas-grid]");
  const cells = block?.querySelector(".site-atlas-cells");
  if (!(block instanceof HTMLElement) || !(cells instanceof HTMLElement)) {
    return null;
  }
  const follow = block.atlasFollow ?? {
    scrolled: 0,
    point: 0,
    line: 0,
    zoom: 1,
    pan: 0,
    nudge: 0,
    end: 0,
  };
  const box = cells.getBoundingClientRect();
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
  const read = [...cells.querySelectorAll(".site-atlas-row")]
    .filter((row) => row instanceof HTMLElement && row.closest("[hidden]") === null)
    .map(ends);
  // The row drawn at the focus line, between it and the next.
  const at = SiteAtlasView.along(
    read.map((row) => row.top),
    box.top + follow.line,
  );
  const left = read.length
    ? SiteAtlasView.curve(
        read.map((row) => row.left),
        at.index,
        at.through,
      )
    : box.left;
  const right = read.length
    ? SiteAtlasView.curve(
        read.map((row) => row.right),
        at.index,
        at.through,
      )
    : box.right;
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
    scale: follow.zoom,
    pan: follow.pan,
    nudge: follow.nudge,
    scrolled: follow.scrolled,
    point: follow.point,
    end: follow.end,
    scrollY: window.scrollY,
    tile: tile instanceof HTMLElement ? tile.getBoundingClientRect().width : 0,
    number:
      number instanceof HTMLElement
        ? Number.parseFloat(getComputedStyle(number).fontSize) * follow.zoom
        : 0,
    room: cells.clientWidth,
    leftEnd: (left - box.left) / cells.clientWidth,
    across: right > left ? (middle - left) / (right - left) : 0,
    lastLeft: read.length ? ((read.at(-1)?.left ?? box.left) - box.left) / cells.clientWidth : 0,
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
