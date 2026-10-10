// The two actions the homepage sets under a table and under the atlas, as drawn: "View
// all results", the link under the recent table, and the atlas's expander. For each,
// its box, how far its centre is from its row's, its computed colours, type, padding
// and corners, its icon's direction, width and side, and what it says: its visible
// label, its name for assistive technology, and for the expander its state and what it
// controls. `null` for a control the page does not have.
() => {
  /** @param {number} value */
  const round = (value) => Math.round(value * 100) / 100;
  /** @param {Element | null} element */
  const read = (element) => {
    if (!(element instanceof HTMLElement)) {
      return null;
    }
    const style = getComputedStyle(element);
    const box = element.getBoundingClientRect();
    const row = element.parentElement?.getBoundingClientRect() ?? null;
    const icon = element.querySelector(".site-icon-arrow");
    const text = element.querySelector("[data-atlas-label]") ?? element.firstChild;
    const textRight =
      text instanceof Element
        ? text.getBoundingClientRect().right
        : text instanceof Text
          ? (() => {
              const range = document.createRange();
              range.selectNodeContents(text);
              return range.getBoundingClientRect().right;
            })()
          : null;
    return {
      box: {
        left: round(box.left),
        right: round(box.right),
        width: round(box.width),
        height: round(box.height),
      },
      centred: row === null ? null : round((box.left + box.right) / 2 - (row.left + row.right) / 2),
      color: style.color,
      background: style.backgroundColor,
      font_px: round(Number.parseFloat(style.fontSize)),
      weight: style.fontWeight,
      family: style.fontFamily,
      padding: style.padding,
      radius: style.borderRadius,
      icon:
        icon instanceof HTMLElement
          ? {
              arrow: icon.dataset.arrow ?? null,
              width: round(icon.getBoundingClientRect().width),
              after_text:
                textRight !== null && icon.getBoundingClientRect().left >= textRight - 0.5,
            }
          : null,
      label: (element.querySelector("[data-atlas-label]") ?? element).textContent?.trim() ?? "",
      name: element.getAttribute("aria-label"),
      expanded: element.getAttribute("aria-expanded"),
      controls: element.getAttribute("aria-controls"),
      classes: [...element.classList],
    };
  };
  return {
    see_all: read(document.querySelector("[data-all-results]")),
    expander: read(document.querySelector("[data-atlas-toggle]")),
  };
};
