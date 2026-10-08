// Input response: the atlas arrives as laid-out static tiles with reserved image
// sizes. Controls change that existing grid only after the reader uses them.
(() => {
  const grid = document.querySelector("[data-atlas-grid]");
  const cells = grid?.querySelector(".site-atlas-cells");
  const rest = grid?.querySelector("[data-atlas-rest]");
  const toggle = grid?.querySelector("[data-atlas-toggle]");
  const tabs = grid?.querySelector("[data-atlas-views]");
  const sizes = grid?.querySelector("[data-atlas-sizes]");
  if (
    !(grid instanceof HTMLElement) ||
    !(cells instanceof HTMLElement) ||
    !(rest instanceof HTMLElement) ||
    !(toggle instanceof HTMLButtonElement) ||
    !(tabs instanceof HTMLElement)
  ) {
    return;
  }
  const views = SiteAtlasView.mount({
    block: grid,
    cells,
    tabs,
    sizes: sizes instanceof HTMLElement ? sizes : null,
  });

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
})();
