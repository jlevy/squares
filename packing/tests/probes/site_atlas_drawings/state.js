// Read the drawing choice and every tile, including currently hidden lazy images.
() => {
  const block = document.querySelector("[data-atlas-grid]");
  if (!(block instanceof HTMLElement)) {
    throw new Error("No atlas block");
  }
  return {
    mode: block.dataset.atlasDrawing,
    tabs: [...block.querySelectorAll("[data-atlas-drawing-tab]")].map((tab) => ({
      label: tab.textContent,
      selected: tab.getAttribute("aria-selected"),
      tabindex: tab.getAttribute("tabindex"),
      controls: tab.getAttribute("aria-controls"),
      focused: document.activeElement === tab,
    })),
    tiles: [...block.querySelectorAll(".site-atlas-cell")].map((tile) => {
      const image = tile.querySelector("img");
      return {
        n: Number(tile.getAttribute("data-atlas-n")),
        href: tile.getAttribute("href"),
        src: image?.getAttribute("src"),
        alt: image?.alt,
        title: image?.title,
        side: Number(tile.getAttribute("data-atlas-side")),
        number_color: getComputedStyle(tile.querySelector(".site-atlas-n") ?? tile).color,
      };
    }),
  };
};
