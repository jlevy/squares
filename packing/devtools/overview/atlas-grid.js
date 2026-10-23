// Input response: the atlas arrives as laid-out static tiles with reserved image
// sizes, every case at once. Controls change that existing grid only after the reader
// uses them.
(() => {
  const grid = document.querySelector("[data-atlas-grid]");
  const cells = grid?.querySelector(".site-atlas-cells");
  const tabs = grid?.querySelector("[data-atlas-views]");
  const sizes = grid?.querySelector("[data-atlas-sizes]");
  const scales = grid?.querySelector("[data-atlas-scales]");
  const drawings = grid?.querySelector("[data-atlas-drawings]");
  if (
    !(grid instanceof HTMLElement) ||
    !(cells instanceof HTMLElement) ||
    !(tabs instanceof HTMLElement)
  ) {
    return;
  }
  const scoped = grid.hasAttribute("data-atlas-preview");
  if (!globalThis.SiteAtlasView) {
    const status = grid.querySelector("[data-homepage-atlas-status]");
    if (status instanceof HTMLElement) {
      status.textContent =
        "The atlas controls did not load; View Visual Atlas opens the dedicated page.";
      status.hidden = false;
    }
    return;
  }
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

  // Prepare immutable drawings a row per frame after first paint and fonts, top row
  // first. Layout never waits for network/decode; a change of drawing reuses the nodes.
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

  // Diagram fragments name tiles separately from the survey's #n-N rows. A fragment
  // lands with its tile focused and centred in the window, panned into the triangle's
  // scroll frame where a narrow screen pans it.
  /** @param {string} hash */
  const reveal = (hash) => {
    if (!/^#atlas-n-\d+$/.test(hash)) {
      return false;
    }
    const tile = document.getElementById(hash.slice(1));
    if (!(tile instanceof HTMLAnchorElement) || !cells.contains(tile)) {
      return false;
    }
    tile.focus({ preventScroll: true });
    tile.scrollIntoView({ block: "center", behavior: "instant" });
    return true;
  };

  // A same-fragment anchor does not emit hashchange. Handling ordinary links on this
  // page lets a reader open a case, and from its popover return to its diagram, with
  // the tile focused again. Keep native navigation for other pages, queries, targets
  // and modifiers.
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
