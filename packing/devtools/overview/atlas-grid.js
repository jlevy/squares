// The homepage's grid of every known-best packing. Its cells arrive in a <template>,
// which the browser parses but does not lay out, and are placed only when the grid
// comes near the viewport, so they cost the page's first paint nothing.
//
// Each cell is a link to its case's record file (`a.site-atlas-cell[data-case]`,
// `cases/11.html`), and nothing here handles a press on one: the page's one case popover
// opens it (`case-popover.js`), with the case's visual summary first, the drawing large,
// the number line of its bounds and the film's facts, then the rest of its record, and
// steps to the neighbouring cases in place. Without scripts a cell goes to the file.
//
// The grid shows the first hundred cases. The button under it places the rest, from a
// second template, the first time it is pressed, and after that shows or hides them.
//
// The tabs over the tiles choose between two views of the one set, the grid and the
// triangle, which `atlas-view.js` lays out and moves between (`SiteAtlasView.mount`).
// They ship `hidden` and show once the tiles are placed.
//
// Beside them, where some case has a regularized view, a second pair chooses the drawing,
// House or Regularized (`SiteAtlasLayer.mount`, `atlas-layer.js`): a case with a
// regularized view has a second tile in a third template, which stands in for its house
// tile wherever the grid places one. Either tile opens the same case record, whose
// drawing is the house one: the regularized layer is the atlas's view, not the record's.
(() => {
  const grid = document.querySelector("[data-atlas-grid]");
  const template = grid?.querySelector("template[data-atlas-first]");
  const restTemplate = grid?.querySelector("template[data-atlas-rest]");
  const toggle = grid?.querySelector("[data-atlas-toggle]");
  const tabs = grid?.querySelector("[data-atlas-views]");
  const controls = grid?.querySelector("[data-atlas-controls]");
  const layerTabs = grid?.querySelector("[data-atlas-layers]");
  const layerTemplate = grid?.querySelector("template[data-atlas-regularized]");
  if (
    !(grid instanceof HTMLElement) ||
    !(template instanceof HTMLTemplateElement) ||
    !(restTemplate instanceof HTMLTemplateElement) ||
    !(toggle instanceof HTMLButtonElement) ||
    !(tabs instanceof HTMLElement)
  ) {
    return;
  }
  const cells = document.createElement("div");
  cells.className = "site-atlas-cells";
  // The rest of the cases, in a box of their own that the grid lays out as if its
  // cells were the grid's own (`display: contents`), so hiding them is one attribute.
  const rest = document.createElement("div");
  rest.className = "site-atlas-rest";
  rest.hidden = true;

  // The view the address names is set here, before any tile is placed, so the page
  // never shows one view and then the other; and so is the drawing.
  const views = SiteAtlasView.mount({ block: grid, cells, tabs });
  const layers =
    layerTabs instanceof HTMLElement && layerTemplate instanceof HTMLTemplateElement
      ? SiteAtlasLayer.mount({ block: grid, cells, tabs: layerTabs, template: layerTemplate })
      : null;

  // The tiles go after the row of tabs, and each placed tile is the drawing the block is
  // in before the box is put in the page.
  const place = () => {
    cells.append(template.content.cloneNode(true), rest);
    layers?.apply();
    (controls instanceof HTMLElement ? controls : tabs).after(cells);
    tabs.hidden = false;
    if (layers !== null && layerTabs instanceof HTMLElement) {
      layerTabs.hidden = false;
    }
    if (toggle.parentElement) {
      toggle.parentElement.hidden = false;
    }
    views.arrange();
  };

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
    if (open && rest.childElementCount === 0) {
      rest.append(restTemplate.content.cloneNode(true));
      layers?.apply();
    }
    views.change(() => {
      rest.hidden = !open;
      relabel(open);
      settle?.();
    });
  };
  toggle.addEventListener("click", () => {
    const open = rest.hidden !== false;
    expandGrid(open, open ? undefined : () => toggle.scrollIntoView({ block: "nearest" }));
  });
  if ("IntersectionObserver" in window) {
    const watch = new IntersectionObserver(
      (entries) => {
        if (entries.some((entry) => entry.isIntersecting)) {
          watch.disconnect();
          place();
        }
      },
      { rootMargin: "800px 0px" },
    );
    watch.observe(grid);
  } else {
    place();
  }
})();
