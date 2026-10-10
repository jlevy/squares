// Input response: the atlas arrives as laid-out static tiles with reserved image
// sizes. Controls change that existing grid only after the reader uses them.
(() => {
  const grid = document.querySelector("[data-atlas-grid]");
  const cells = grid?.querySelector(".site-atlas-cells");
  const rest = grid?.querySelector("[data-atlas-rest]");
  const toggle = grid?.querySelector("[data-atlas-toggle]");
  const tabs = grid?.querySelector("[data-atlas-views]");
  const sizes = grid?.querySelector("[data-atlas-sizes]");
  const scales = grid?.querySelector("[data-atlas-scales]");
  if (
    !(grid instanceof HTMLElement) ||
    !(cells instanceof HTMLElement) ||
    !(rest instanceof HTMLElement) ||
    !(toggle instanceof HTMLButtonElement) ||
    !(tabs instanceof HTMLElement)
  ) {
    return;
  }
  const tiles = [...cells.querySelectorAll("a.site-atlas-cell")];
  const first = Number(grid.dataset.atlasFirst) || 100;
  let expanded = false;

  // The button reads Show More with the double chevron down, and once the rest show,
  // Show Less with the chevron up; its name for assistive technology says what each
  // does and how many cases that is, from the names the page ships.
  const toggleLabel = toggle.querySelector("[data-atlas-label]");
  const toggleChevron = toggle.querySelector(".site-icon-arrow");
  /** @param {boolean} open */
  const relabel = (open) => {
    toggle.setAttribute("aria-expanded", String(open));
    toggle.setAttribute(
      "aria-label",
      (open ? toggle.dataset.nameLess : toggle.dataset.nameMore) ?? "",
    );
    if (toggleLabel !== null) {
      toggleLabel.textContent = (open ? toggle.dataset.labelLess : toggle.dataset.labelMore) ?? "";
    }
    if (toggleChevron instanceof HTMLElement) {
      toggleChevron.dataset.arrow = open ? "double-up" : "double-down";
    }
  };

  // Complete physical grid rows near the nominal limit, or mathematical square
  // rows in Triangle. Only boundary anchors move; stable links retain their focus.
  const completePreview = () => {
    const triangle = grid.dataset.atlasView === "triangle";
    // Inline per-line state still describes the previous arrangement here. Use
    // the shared capacity calculation with the current width/size tokens, so the
    // completed prefix and the layout that follows use the same columns.
    const root = Number.parseFloat(getComputedStyle(document.documentElement).fontSize);
    const style = getComputedStyle(cells);
    const columns = SiteAtlasView.perLineAt(
      cells.getBoundingClientRect().width,
      SiteAtlasView.lengthPx(style.getPropertyValue("--site-atlas-cell-min"), root),
      Number.POSITIVE_INFINITY,
      Number.parseFloat(style.getPropertyValue("--site-atlas-scale")),
      SiteAtlasView.lengthPx(style.getPropertyValue("--site-atlas-reference-gap"), root),
    );
    let count = triangle
      ? Math.round(Math.sqrt(first)) ** 2
      : Math.max(columns, Math.round(first / columns) * columns);
    const direct = Number(grid.dataset.atlasPreviewCount) || first;
    // A stepped popover still returns to its original opener. Retain the visible
    // prefix while it is open, rounding up so that origin cannot become hidden.
    if (!expanded && count < direct && document.querySelector("#pop-case:popover-open")) {
      count = triangle ? Math.ceil(Math.sqrt(direct)) ** 2 : Math.ceil(direct / columns) * columns;
    }
    count = Math.min(tiles.length, count);
    grid.dataset.atlasPreviewCount = String(count);
    toggle.dataset.nameLess = `Show less: the first ${count}`;
    const shown = expanded ? tiles.length : count;
    const focused = document.activeElement;
    // Keep the server's row/segment structure and all link identities intact.
    rest.hidden = false;
    for (const tile of tiles) {
      tile.toggleAttribute("hidden", Number(tile.getAttribute("data-atlas-n")) > shown);
    }
    for (const row of cells.querySelectorAll(".site-atlas-row")) {
      row.toggleAttribute(
        "hidden",
        [...row.querySelectorAll(".site-atlas-cell")].every((tile) => tile.hasAttribute("hidden")),
      );
    }
    cells.style.setProperty("--site-atlas-widest", String(SiteAtlasView.widest(shown)));
    cells.style.setProperty(
      "--site-atlas-extra",
      expanded ? "var(--site-atlas-last-extra)" : "var(--site-atlas-first-extra)",
    );
    if (focused instanceof HTMLElement && focused.closest("[hidden]") !== null) {
      const last = tiles[shown - 1];
      if (last instanceof HTMLElement) {
        last.focus({ preventScroll: true });
      }
    }
    relabel(expanded);
  };
  const views = SiteAtlasView.mount({
    block: grid,
    cells,
    tabs,
    sizes: sizes instanceof HTMLElement ? sizes : null,
    scales: scales instanceof HTMLElement ? scales : null,
    beforeArrange: completePreview,
  });

  // Showing or hiding the rest changes where the triangle's tiles stand, since its
  // longest row sets how many a line holds, so it is a change of layout like a change
  // of view: the tiles that stay move, and the ones that arrive fade in. Collapsing
  // takes away everything above the button but the first hundred, so the page would
  // land far below it: `settle` brings the button back to where the reader is, as part
  // of the same change.
  /**
   * @param {boolean} open
   * @param {() => void} [settle]
   */
  const expandGrid = (open, settle) => {
    views.change(() => {
      expanded = open;
      // Settle scrolling against the final completed rows and triangle positions.
      views.arrange();
      settle?.();
    });
  };
  toggle.addEventListener("click", () => {
    const open = !expanded;
    expandGrid(open, open ? undefined : () => toggle.scrollIntoView({ block: "nearest" }));
  });

  // Diagram fragments name tiles separately from the survey's #n-N rows. Even a
  // tile among the first hundred opens the complete atlas before we place it in the
  // viewport. `change` arranges after its mutation; finish the tile moves only then,
  // so a fragment lands on the final layout rather than a tile still in transit.
  /** @param {string} hash */
  const reveal = (hash) => {
    if (!/^#atlas-n-\d+$/.test(hash)) {
      return false;
    }
    const tile = document.getElementById(hash.slice(1));
    if (!(tile instanceof HTMLAnchorElement) || !cells.contains(tile)) {
      return false;
    }
    expandGrid(true);
    for (const animation of cells.getAnimations({ subtree: true })) {
      animation.finish();
    }
    tile.focus({ preventScroll: true });
    tile.scrollIntoView({ block: "center", behavior: "instant" });
    return true;
  };

  // A same-fragment anchor does not emit hashchange. Handling ordinary links on this
  // page also lets a reader collapse the atlas, open the same case, and return to its
  // diagram. Keep native navigation for other pages, queries, targets and modifiers.
  document.addEventListener("click", (event) => {
    if (
      event.defaultPrevented ||
      event.button !== 0 ||
      event.metaKey ||
      event.ctrlKey ||
      event.shiftKey ||
      event.altKey ||
      !(event.target instanceof Element)
    ) {
      return;
    }
    const link = event.target.closest("a[href]");
    if (!(link instanceof HTMLAnchorElement) || (link.target !== "" && link.target !== "_self")) {
      return;
    }
    const url = new URL(link.href, document.baseURI);
    if (
      url.origin !== location.origin ||
      url.pathname !== location.pathname ||
      url.search !== location.search ||
      !reveal(url.hash)
    ) {
      return;
    }
    event.preventDefault();
    if (url.hash !== location.hash) {
      // Native fragment navigation updates :target as well as history. hashchange
      // then reapplies the settled placement after the browser's fragment scroll.
      location.hash = url.hash;
    }
  });
  window.addEventListener("hashchange", () => reveal(location.hash));
  reveal(location.hash);
})();
