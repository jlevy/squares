// Completed previews and persistent anchors, including focus after a boundary moves.
(/** @type {{install?: boolean}} */ options) => {
  const block = document.querySelector("[data-atlas-grid]");
  const cells = block?.querySelector(".site-atlas-cells");
  const toggle = block?.querySelector("[data-atlas-toggle]");
  if (!(block instanceof HTMLElement) || !(cells instanceof HTMLElement)) {
    throw new Error("Missing dedicated Atlas");
  }
  if (options.install) {
    const original = [...cells.querySelectorAll("a.site-atlas-cell")];
    const drawings = original.map((tile) => tile.querySelector("img"));
    cells.addEventListener("atlas-test-identity", () => {
      const current = [...cells.querySelectorAll("a.site-atlas-cell")];
      block.dataset.testIdentity = String(
        current.length === original.length &&
          current.every(
            (tile, index) =>
              tile === original[index] && tile.querySelector("img") === drawings[index],
          ),
      );
    });
  }
  cells.dispatchEvent(new Event("atlas-test-identity"));
  const tiles = [...cells.querySelectorAll("a.site-atlas-cell")];
  const shown = tiles.filter((tile) => tile.getClientRects().length > 0);
  const box = toggle?.getBoundingClientRect();
  const focus = document.activeElement;
  return {
    view: block.dataset.atlasView,
    root_view: document.documentElement.dataset.siteAtlasView ?? null,
    size: block.dataset.atlasSize,
    columns: getComputedStyle(cells).gridTemplateColumns.trim().split(/\s+/).length,
    total: tiles.length,
    shown: shown.map((tile) => Number(tile.getAttribute("data-atlas-n"))),
    direct: shown.length,
    expanded: toggle?.getAttribute("aria-expanded"),
    collapsed: toggle?.getAttribute("aria-expanded") === "false",
    name: toggle?.getAttribute("aria-label"),
    collapse_name: toggle?.getAttribute("data-name-less"),
    same_nodes: block.dataset.testIdentity === "true",
    selected: block
      .querySelector('[data-atlas-tab][aria-selected="true"]')
      ?.getAttribute("data-atlas-tab"),
    focus: focus?.getAttribute("data-case"),
    focus_visible: focus instanceof HTMLElement && focus.getClientRects().length > 0,
    toggle_visible: Boolean(box && box.top >= 0 && box.bottom <= window.innerHeight),
    popover_open: document.querySelector("#pop-case:popover-open") !== null,
    search: location.search,
    hash: location.hash,
  };
};
