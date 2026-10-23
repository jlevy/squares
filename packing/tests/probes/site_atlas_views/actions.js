// Two of the homepage's actions as drawn: "View all results", the link under the recent
// table, and "View Visual Atlas", the link to the Atlas page under the atlas. For each,
// its box, its computed colours, type, padding and corners, its icon's direction, width
// and side, and its visible label. `null` for an action the page does not have.
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
    const icon = element.querySelector(".site-icon-arrow");
    const text = element.firstChild;
    const textRight =
      text instanceof Text
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
      row_gap: element.parentElement ? getComputedStyle(element.parentElement).columnGap : null,
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
      label: element.textContent?.trim() ?? "",
      classes: [...element.classList],
    };
  };
  return {
    see_all: read(document.querySelector("[data-all-results]")),
    atlas: read(document.querySelector('.site-homepage-atlas-actions a[href="atlas.html"]')),
  };
};
