async () => {
  await document.fonts.ready;
  const inner = document.querySelector(".site-nav-inner");
  if (!inner) {
    throw new Error("The page has no navigation track");
  }
  const context = document.createElement("canvas").getContext("2d");
  if (!context) {
    throw new Error("The navigation ink probe needs a canvas context");
  }
  return [...inner.children].map((item) => {
    const box = item.getBoundingClientRect();
    const button = item.querySelector(".site-theme-button");
    const reference = item.matches("a[data-page]") ? item : button;
    let baseline = null;
    let inkCenter = null;
    let capCenter = null;
    if (reference) {
      const marker = document.createElement("span");
      Object.assign(marker.style, {
        display: "inline-block",
        width: "0",
        height: "0",
        verticalAlign: "baseline",
      });
      reference.append(marker);
      baseline = marker.getBoundingClientRect().bottom;
      marker.remove();
      const style = getComputedStyle(reference);
      context.font = `${style.fontWeight} ${style.fontSize} ${style.fontFamily}`;
      const ink = context.measureText(button ? "GitHub" : (item.textContent?.trim() ?? ""));
      const capital = context.measureText("H");
      inkCenter = baseline + (ink.actualBoundingBoxDescent - ink.actualBoundingBoxAscent) / 2;
      capCenter = baseline - capital.actualBoundingBoxAscent / 2;
    }
    const icon = item.querySelector(".site-theme-button svg");
    return {
      label: (item.getAttribute("data-page") ?? item.className).trim(),
      top: box.top,
      bottom: box.bottom,
      width: box.width,
      left: box.left,
      baseline,
      inkCenter,
      capCenter,
      iconBottom: icon?.getBoundingClientRect().bottom ?? null,
      iconCenter: icon
        ? (icon.getBoundingClientRect().top + icon.getBoundingClientRect().bottom) / 2
        : null,
      buttonWidth: button?.getBoundingClientRect().width ?? null,
      buttonHeight: button?.getBoundingClientRect().height ?? null,
    };
  });
};
