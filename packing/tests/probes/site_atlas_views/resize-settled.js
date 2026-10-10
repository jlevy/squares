// ResizeObserver schedules arrangement in the following animation frame. Existing
// animations alone can be quiet before that work has committed. Require the current
// CSS capacity, committed columns, and unchanged geometry over consecutive frames.
async (/** @type {{width: number}} */ { width }) => {
  const block = document.querySelector("[data-atlas-grid]");
  const cells = block?.querySelector(".site-atlas-cells");
  if (!(block instanceof HTMLElement) || !(cells instanceof HTMLElement)) {
    return false;
  }
  const frame = () => new Promise((resolve) => requestAnimationFrame(resolve));
  const read = () => {
    if (window.innerWidth !== width || block.dataset.atlasView !== "grid") {
      return null;
    }
    const style = getComputedStyle(cells);
    const root = Number.parseFloat(getComputedStyle(document.documentElement).fontSize);
    /** @param {string} property */
    const pixels = (property) => {
      const value = style.getPropertyValue(property).trim();
      return Number.parseFloat(value) * (value.endsWith("rem") ? root : 1);
    };
    const minimum = pixels("--site-atlas-cell-min");
    const gap = pixels("--site-atlas-reference-gap");
    const scale = Number.parseFloat(style.getPropertyValue("--site-atlas-scale"));
    const box = cells.getBoundingClientRect();
    const capacity = Math.max(1, Math.floor((box.width + gap) / (minimum * scale + gap)));
    const committed = Number(cells.style.getPropertyValue("--site-atlas-per-line"));
    const columns = style.gridTemplateColumns.trim().split(/\s+/).length;
    if (!(minimum > 0 && scale > 0) || capacity !== committed || capacity !== columns) {
      return null;
    }
    return JSON.stringify([box.width, box.height, capacity, block.dataset.atlasPreviewCount]);
  };
  await frame();
  const first = read();
  await frame();
  const second = read();
  await frame();
  return first !== null && first === second && second === read();
};
