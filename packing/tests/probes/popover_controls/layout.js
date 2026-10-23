/** @param {HTMLElement} panel */
(panel) => {
  const expand = panel.querySelector(".site-popover-expand");
  const close = panel.querySelector(".site-popover-close");
  if (!(expand instanceof HTMLElement) || !(close instanceof HTMLElement)) {
    throw new Error("popover header is missing its full-page or close control");
  }
  /** @param {Element} element */
  const box = (element) => {
    const rect = element.getBoundingClientRect();
    return { left: rect.left, right: rect.right, width: rect.width, height: rect.height };
  };
  /** @param {Element} element */
  const hit = (element) => {
    const rect = element.getBoundingClientRect();
    return element.contains(
      document.elementFromPoint(rect.left + rect.width / 2, rect.top + rect.height / 2),
    );
  };
  /** @param {Element} element */
  const iconSize = (element) => {
    const icon = element.querySelector("svg");
    if (icon === null) {
      throw new Error("popover header has no icon");
    }
    const rect = icon.getBoundingClientRect();
    return { width: rect.width, height: rect.height };
  };
  /** @param {Element} element */
  const glyphWidth = (element) => {
    const icon = element.querySelector("svg");
    if (!(icon instanceof SVGGraphicsElement)) {
      throw new Error("popover header has no SVG glyph");
    }
    return icon.getBBox().width;
  };
  const title = panel.querySelector("article > h1");
  const titleRange = document.createRange();
  if (title) {
    titleRange.selectNodeContents(title);
  }
  const controls = [expand.getBoundingClientRect(), close.getBoundingClientRect()];
  const titleOverlapsControls =
    title !== null &&
    [...titleRange.getClientRects()].some((text) =>
      controls.some(
        (control) =>
          text.left < control.right - 0.5 &&
          text.right > control.left + 0.5 &&
          text.top < control.bottom - 0.5 &&
          text.bottom > control.top + 0.5,
      ),
    );
  return {
    titleOverlapsControls,
    expand: box(expand),
    close: box(close),
    expandIcon: iconSize(expand),
    closeIcon: iconSize(close),
    expandGlyphWidth: glyphWidth(expand),
    closeGlyphWidth: glyphWidth(close),
    hitExpand: hit(expand),
    hitClose: hit(close),
    pageWidth: document.documentElement.scrollWidth,
  };
};
