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
    ].map((chooser) => {
      const tab = chooser.querySelector('[role="tab"]');
      if (!(tab instanceof HTMLElement)) {
        throw new Error("Each visible Atlas chooser needs an actual tab");
      }
      const style = getComputedStyle(tab);
      return {
        ...box(chooser),
        fontSize: style.fontSize,
        lineHeight: style.lineHeight,
        weight: style.fontWeight,
        padding: style.padding,
      };
    }),
    columns: [...legend.querySelectorAll(".site-atlas-legend-column")].map((column) => ({
      box: box(column),
      items: [...column.querySelectorAll(".site-atlas-legend-item")].map((item) => ({
        box: box(item),
        textAlign: getComputedStyle(item).textAlign,
        alignment: getComputedStyle(item).alignItems,
        lineHeight: Number.parseFloat(getComputedStyle(item).lineHeight),
        swatches: [...item.querySelectorAll(".site-atlas-swatch")].map((swatch) => {
          const rect = swatch.getBoundingClientRect();
          const label = document.createRange();
          label.selectNodeContents(swatch);
          return {
            width: rect.width,
            height: rect.height,
            top: rect.top,
            bottom: rect.bottom,
            labelFontSize: Number.parseFloat(getComputedStyle(swatch).fontSize),
            labelWidth: label.getBoundingClientRect().width,
          };
        }),
      })),
    })),
  };
};
