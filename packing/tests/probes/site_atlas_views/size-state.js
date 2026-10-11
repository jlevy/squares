// First CSS paint and mounted size state share one reader, including the scoped preview.
(/** @type {{size?: string} | null} */ wanted) => {
  const block = document.querySelector(".site-atlas-grid");
  const cells = block?.querySelector(".site-atlas-cells");
  if (!(block instanceof HTMLElement) || !(cells instanceof HTMLElement)) {
    return null;
  }
  if (wanted?.size && block.dataset.atlasSize !== wanted.size) {
    return null;
  }
  const style = getComputedStyle(cells);
  return {
    size: block.dataset.atlasSize,
    explicit: block.hasAttribute("data-atlas-size-explicit"),
    root_size: document.documentElement.dataset.siteAtlasSize ?? null,
    scale: Number.parseFloat(style.getPropertyValue("--site-atlas-scale")),
    tile_width: cells.querySelector(".site-atlas-cell")?.getBoundingClientRect().width,
    columns: Number.parseFloat(style.getPropertyValue("--site-atlas-per-line")),
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
