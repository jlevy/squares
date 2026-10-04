// An init script: note the state of the atlas at the moment its box of tiles is first put
// in the page, which is before the browser has drawn a tile. A page opened on
// `?atlas=triangle` must already be in the triangle then, with its tiles arranged, or it
// would show the grid first and then the triangle; and one opened on
// `?layer=regularized` must already show its regularized tiles. The notes are left on
// `atlasViewsSeen` for `seen` to return.
() => {
  /** @type {AtlasViewSeen[]} */
  const seen = [];
  globalThis.atlasViewsSeen = seen;
  new MutationObserver((records) => {
    for (const record of records) {
      for (const node of record.addedNodes) {
        if (node instanceof HTMLElement && node.classList.contains("site-atlas-cells")) {
          const block = node.closest("[data-atlas-grid]");
          seen.push({
            view: block instanceof HTMLElement ? (block.dataset.atlasView ?? null) : null,
            layer: block instanceof HTMLElement ? (block.dataset.atlasLayer ?? null) : null,
            per_line: node.style.getPropertyValue("--site-atlas-per-line"),
            tiles: node.querySelectorAll(".site-atlas-cell").length,
            regularized: node.querySelectorAll('.site-atlas-cell[data-atlas-layer="regularized"]')
              .length,
            moving: document.getAnimations().length,
          });
        }
      }
    }
  }).observe(document, { childList: true, subtree: true });
};
