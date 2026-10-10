// Measure the visible chooser lines and legend content, not their full-width wrappers.
() => {
  /** @param {Element} element */
  const box = (element) => {
    const rect = element.getBoundingClientRect();
    return { left: rect.left, right: rect.right, top: rect.top, bottom: rect.bottom };
  };
  const controls = document.querySelector("[data-atlas-controls]");
  const legend = document.querySelector("[data-atlas-legend]");
  if (!controls || !legend) {
    throw new Error("the atlas controls and shared legend must be present");
  }
  return {
    controls: box(controls),
    choosers: [
      ...controls.querySelectorAll("[data-atlas-views], [data-atlas-sizes], [data-atlas-scales]"),
    ].map(box),
    columns: [...legend.querySelectorAll(".site-atlas-legend-column")].map((column) => ({
      box: box(column),
      items: [...column.querySelectorAll(".site-atlas-legend-item")].map((item) => ({
        box: box(item),
        textAlign: getComputedStyle(item).textAlign,
      })),
    })),
  };
};
