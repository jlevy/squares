// Prepare native poster tiles once, then use the Atlas page's layout and animation.
// The inert compressed source keeps the HTML bounded; input never fetches or waits.
(() => {
  const grid = document.querySelector("[data-atlas-preview]");
  const cells = grid?.querySelector(".site-atlas-cells");
  const rest = cells?.querySelector("[data-atlas-rest]");
  const payload = grid?.querySelector("[data-homepage-atlas-gzip]");
  const toggle = document.querySelector("[data-homepage-atlas-toggle]");
  const label = toggle?.querySelector("[data-homepage-atlas-label]");
  const chevron = toggle?.querySelector(".site-icon-arrow");
  const status = document.querySelector("[data-homepage-atlas-status]");
  if (
    !(grid instanceof HTMLElement) ||
    !(cells instanceof HTMLElement) ||
    !(rest instanceof HTMLElement) ||
    !(payload instanceof HTMLTemplateElement) ||
    !(toggle instanceof HTMLButtonElement) ||
    !(label instanceof HTMLElement) ||
    !(status instanceof HTMLElement) ||
    !globalThis.SiteAtlasView
  ) {
    return;
  }
  const initialCount = cells.querySelectorAll("a[data-case]").length;
  const left = Number(grid.dataset.atlasGridLeft);
  const top = Number(grid.dataset.atlasGridTop);
  const columnPitch = Number(grid.dataset.atlasColumnPitch);
  const rowPitch = Number(grid.dataset.atlasRowPitch);
  const cardWidth = Number(grid.dataset.atlasCardWidth);
  const cardHeight = Number(grid.dataset.atlasCardHeight);
  let count = initialCount;

  const relabel = () => {
    const full = count === 324;
    const next = count < 100 ? 100 : 324;
    grid.dataset.atlasCount = String(count);
    toggle.setAttribute("aria-expanded", String(count > initialCount));
    toggle.setAttribute(
      "aria-label",
      full
        ? `Show less: collapse from ${count} to ${initialCount} cases (${Math.sqrt(initialCount)} rows)`
        : `Show more: expand from ${count} to ${next} cases (${Math.sqrt(next)} rows)`,
    );
    label.textContent = full ? "Show Less" : "Show More";
    if (chevron instanceof HTMLElement) {
      chevron.dataset.arrow = full ? "double-up" : "double-down";
    }
  };

  const prepare = async () => {
    const bytes = Uint8Array.from(atob(payload.content.textContent?.trim() ?? ""), (byte) =>
      byte.charCodeAt(0),
    );
    const stream = new Blob([bytes]).stream().pipeThrough(new DecompressionStream("gzip"));
    const parsed = new DOMParser().parseFromString(
      await new Response(stream).text(),
      "image/svg+xml",
    );
    const cards = [...parsed.querySelectorAll('g[data-feature="packing-card"]')];
    if (
      parsed.documentElement.localName !== "svg" ||
      cards.length !== 324 ||
      cards.some((card, index) => Number(card.getAttribute("data-n")) !== index + 1)
    ) {
      throw new Error("The prepared Atlas has no complete packing graphic");
    }
    const additional = document.createDocumentFragment();
    for (const card of cards.slice(initialCount)) {
      const n = Number(card.getAttribute("data-n"));
      const x = left + columnPitch * Number(card.getAttribute("data-column"));
      const y = top + rowPitch * Number(card.getAttribute("data-row"));
      const link = document.createElement("a");
      link.className = "site-atlas-cell";
      link.href = new URL(`cases/${n}.html`, document.baseURI).href;
      link.dataset.case = String(n);
      link.dataset.atlasN = String(n);
      link.setAttribute("aria-label", `Case ${n}: packing and bounds`);
      const svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
      svg.setAttribute("width", String(cardWidth));
      svg.setAttribute("height", String(cardHeight));
      svg.setAttribute("viewBox", `${x} ${y} ${cardWidth} ${cardHeight}`);
      svg.setAttribute("aria-hidden", "true");
      svg.setAttribute("data-homepage-atlas-svg", "");
      const background = document.createElementNS("http://www.w3.org/2000/svg", "rect");
      background.setAttribute("data-feature", "atlas-background");
      background.setAttribute("x", String(x));
      background.setAttribute("y", String(y));
      background.setAttribute("width", String(cardWidth));
      background.setAttribute("height", String(cardHeight));
      background.setAttribute("fill", "#ffffff");
      svg.append(background, card);
      link.append(svg);
      additional.append(link);
    }
    rest.append(additional);
    payload.remove();
    return globalThis.SiteAtlasView.mount({
      block: grid,
      cells,
      tabs: null,
      sizes: null,
      scoped: true,
    });
  };

  void prepare().then(
    (views) => {
      const tiles = [...cells.querySelectorAll("a.site-atlas-cell")];
      toggle.addEventListener("click", () => {
        const next = count < 100 ? 100 : count < tiles.length ? tiles.length : initialCount;
        views.change(() => {
          if (next > count) {
            rest.before(...tiles.slice(count, next));
          } else {
            rest.prepend(...tiles.slice(next, count));
          }
          count = next;
          cells.style.setProperty("--site-atlas-widest", String(SiteAtlasView.widest(count)));
          relabel();
          if (count === initialCount) {
            views.arrange();
            toggle.scrollIntoView({ block: "nearest", behavior: "instant" });
          }
        });
      });
      relabel();
      grid.dataset.atlasReady = "true";
      toggle.hidden = false;
    },
    () => {
      status.textContent =
        "Use Explore the atlas to open the complete page; the preview is still available.";
      status.hidden = false;
    },
  );
})();
