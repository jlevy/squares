// Note the query-selected geometry once the static document is parsed. The separate
// initial probe withholds atlas programs to prove the stylesheet places it directly.
() => {
  globalThis.atlasViewsSeen = [];
  document.addEventListener(
    "DOMContentLoaded",
    () => {
      const cells = document.querySelector(".site-atlas-cells");
      if (!(cells instanceof HTMLElement)) {
        return;
      }
      const root = document.documentElement;
      globalThis.atlasViewsSeen?.push({
        view: root.dataset.siteAtlasView === "triangle" ? "triangle" : "grid",
        size: root.dataset.siteAtlasSize ?? "small",
        scale: root.dataset.siteAtlasScale ?? "fixed",
        per_line: String(
          Math.round(
            (cells.getBoundingClientRect().width +
              Number.parseFloat(getComputedStyle(cells).columnGap)) /
              ((cells.querySelector(".site-atlas-cell")?.getBoundingClientRect().width ?? 1) +
                Number.parseFloat(getComputedStyle(cells).columnGap)),
          ),
        ),
        tiles: [...cells.querySelectorAll(".site-atlas-cell")].filter(
          (tile) => tile.getClientRects().length > 0,
        ).length,
        moving: document
          .getAnimations()
          .filter(
            (animation) =>
              !(animation instanceof CSSTransition) &&
              animation.effect instanceof KeyframeEffect &&
              animation.effect.target?.matches(".site-atlas-cell") === true,
          ).length,
      });
    },
    { once: true },
  );
};
