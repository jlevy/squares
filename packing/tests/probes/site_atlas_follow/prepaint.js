// What the stylesheet alone draws for the atlas, with or without its programs: the size's
// scale, the first tile's width and the first case number's size, and the attributes the
// head bootstrap and the programs set.
() => {
  const block = document.querySelector("[data-atlas-grid]");
  const cells = block?.querySelector(".site-atlas-cells");
  const tile = cells?.querySelector(".site-atlas-cell");
  const number = cells?.querySelector(".site-atlas-n");
  if (
    !(block instanceof HTMLElement) ||
    !(cells instanceof HTMLElement) ||
    !(tile instanceof HTMLElement) ||
    !(number instanceof HTMLElement)
  ) {
    return null;
  }
  return {
    armed: document.documentElement.hasAttribute("data-site-atlas-follow"),
    follow: block.dataset.atlasFollow ?? null,
    zoomed: block.hasAttribute("data-atlas-zoom"),
    size: block.dataset.atlasSize ?? null,
    scale: Number.parseFloat(getComputedStyle(cells).getPropertyValue("--site-atlas-scale")),
    tile: tile.getBoundingClientRect().width,
    number: Number.parseFloat(getComputedStyle(number).fontSize),
  };
};
