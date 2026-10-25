// Input response: the atlas arrives as laid-out static tiles with reserved image
// sizes, every case on either page. Controls change that existing grid only after the
// reader uses them.
(() => {
  const grid = document.querySelector("[data-atlas-grid]");
  const cells = grid?.querySelector(".site-atlas-cells");
  const tabs = grid?.querySelector("[data-atlas-views]");
  const sizes = grid?.querySelector("[data-atlas-sizes]");
  const scales = grid?.querySelector("[data-atlas-scales]");
  const drawings = grid?.querySelector("[data-atlas-drawings]");
  // Without the views' script the static tiles stay as the stylesheet sets them, every
  // case a link to its record.
  if (
    !(grid instanceof HTMLElement) ||
    !(cells instanceof HTMLElement) ||
    !(tabs instanceof HTMLElement) ||
    !globalThis.SiteAtlasView
  ) {
    return;
  }
  const scoped = grid.hasAttribute("data-atlas-preview");
  const views = SiteAtlasView.mount({
    block: grid,
    cells,
    tabs,
    sizes: sizes instanceof HTMLElement ? sizes : null,
    scales: scales instanceof HTMLElement ? scales : null,
    drawings: drawings instanceof HTMLElement ? drawings : null,
    onDrawingChange: () => {
      generation += 1;
      for (const image of images) {
        if (image.dataset.atlasImageState !== "ready") {
          delete image.dataset.atlasImageState;
        }
      }
      decoded = images.filter((image) => image.dataset.atlasImageState === "ready").length;
      grid.dataset.atlasImagesReady = String(decoded);
      pendingRows.splice(0, pendingRows.length, ...rows);
      prepare();
    },
    scoped,
  });

  // Prepare immutable drawings a row per frame after first paint and fonts. Layout
  // never waits for network/decode; a change of drawing reuses the same image nodes.
  const rows = [...cells.querySelectorAll(".site-atlas-row")];
  const images = [...cells.querySelectorAll("img")];
  const pendingRows = [...rows];
  let preparing = false;
  let decoded = 0;
  let generation = 0;
  /** @param {Element} row */
  const prepareRow = (row) => {
    for (const image of row.querySelectorAll("img")) {
      if (image.dataset.atlasImageState) {
        continue;
      }
      image.dataset.atlasImageState = "preparing";
      image.loading = "eager";
      if (image.fetchPriority !== "high") {
        image.fetchPriority = "low";
      }
      const source = image.src;
      const started = generation;
      void image.decode().then(
        () => {
          if (
            started !== generation ||
            image.src !== source ||
            image.dataset.atlasImageState !== "preparing"
          ) {
            return;
          }
          image.dataset.atlasImageState = "ready";
          decoded += 1;
          grid.dataset.atlasImagesReady = String(decoded);
        },
        () => {
          if (
            started !== generation ||
            image.src !== source ||
            image.dataset.atlasImageState !== "preparing"
          ) {
            return;
          }
          // A missing drawing keeps its canonical case link and reserved geometry.
          image.dataset.atlasImageState = "failed";
        },
      );
    }
  };
  const prepareNext = () => {
    const row = pendingRows.shift();
    if (row) {
      prepareRow(row);
      requestAnimationFrame(prepareNext);
    } else {
      preparing = false;
    }
  };
  const prepare = () => {
    if (!preparing && pendingRows.length > 0) {
      preparing = true;
      requestAnimationFrame(prepareNext);
    }
  };
  void views.fontsReady.then(prepare);

  // Diagram fragments name tiles separately from the survey's #n-N rows. A change of
  // layout may still be moving the tiles: finish the moves first, so a fragment lands
  // on the final layout rather than a tile still in transit.
  /** @param {string} hash */
  const reveal = (hash) => {
    if (!/^#atlas-n-\d+$/.test(hash)) {
      return false;
    }
    const tile = document.getElementById(hash.slice(1));
    if (!(tile instanceof HTMLAnchorElement) || !cells.contains(tile)) {
      return false;
    }
    // A tile the reader asked for by name stays where it is put.
    views.hold();
    for (const animation of cells.getAnimations({ subtree: true })) {
      animation.finish();
    }
    tile.focus({ preventScroll: true });
    tile.scrollIntoView({ block: "center", behavior: "instant" });
    return true;
  };

  // A same-fragment anchor does not emit hashchange. Handling ordinary links on this
  // page also lets a reader who has scrolled on open the same case and return to its
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
  grid.dataset.atlasReady = "true";
})();
