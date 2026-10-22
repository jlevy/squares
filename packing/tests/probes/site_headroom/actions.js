// Read actual capital-letter ink against the shared action's border box. A marker
// belongs inside the text's flex item; a direct flex child is not a text baseline.
async (labelOffset = 0) => {
  await document.fonts.ready;
  const context = document.createElement("canvas").getContext("2d");
  if (!context) {
    throw new Error("Action ink needs a canvas context");
  }
  return [...document.querySelectorAll(".site-action, .site-popover-action")]
    .filter((action) => action.getClientRects().length > 0)
    .map((action) => {
      const original = action.getBoundingClientRect();
      const existing = action.querySelector("[data-atlas-label]");
      const label = existing ?? document.createElement("span");
      const text = existing
        ? null
        : [...action.childNodes].find((node) => node instanceof Text && node.textContent?.trim());
      if (!existing) {
        if (!text) {
          throw new Error("The action has no label text");
        }
        text.before(label);
        label.append(text);
      }
      // Move the visible label for sensitivity controls without resizing its hit area.
      const originalStyle = label.getAttribute("style");
      if (labelOffset) {
        label.setAttribute("style", `${originalStyle ?? ""}; translate: 0 ${labelOffset}px`);
      }
      const marker = document.createElement("span");
      Object.assign(marker.style, {
        display: "inline-block",
        width: "0",
        height: "0",
        verticalAlign: "baseline",
      });
      label.append(marker);
      const baseline = marker.getBoundingClientRect().bottom;
      const style = getComputedStyle(label);
      context.font = `${style.fontWeight} ${style.fontSize} ${style.fontFamily}`;
      const content = label.textContent?.trim() ?? "";
      const rendered = style.textTransform === "uppercase" ? content.toUpperCase() : content;
      const ink = context.measureText(rendered);
      const box = action.getBoundingClientRect();
      const top = baseline - ink.actualBoundingBoxAscent;
      const bottom = baseline + ink.actualBoundingBoxDescent;
      const icon = action.querySelector(".site-icon-arrow")?.getBoundingClientRect();
      const report = {
        label: rendered,
        fontSize: style.fontSize,
        lineHeight: style.lineHeight,
        paddingTop: getComputedStyle(action).paddingTop,
        paddingBottom: getComputedStyle(action).paddingBottom,
        height: box.height,
        originalHeight: original.height,
        baseline,
        ascent: ink.actualBoundingBoxAscent,
        descent: ink.actualBoundingBoxDescent,
        fontAscent: ink.fontBoundingBoxAscent,
        fontDescent: ink.fontBoundingBoxDescent,
        topGap: top - box.top,
        bottomGap: box.bottom - bottom,
        centerOffset: (top + bottom - box.top - box.bottom) / 2,
        iconOffset: icon ? (icon.top + icon.bottom - box.top - box.bottom) / 2 : null,
      };
      marker.remove();
      if (originalStyle === null) {
        label.removeAttribute("style");
      } else {
        label.setAttribute("style", originalStyle);
      }
      if (!existing) {
        label.replaceWith(...label.childNodes);
      }
      return report;
    });
};
