// The native 53-square packing stays centered in a compact hero.
async () => {
  await document.fonts.ready;
  const figure = document.querySelector(".site-homepage-hero .site-hero-figure");
  const group = figure?.querySelector(".site-hero-packings");
  if (!(figure instanceof HTMLElement) || !(group instanceof HTMLElement)) {
    throw new Error("Missing homepage hero");
  }
  const frame = figure.getBoundingClientRect();
  const parent = figure.parentElement?.getBoundingClientRect();
  const rects = [...group.querySelectorAll("a[data-case]")].map((link) => {
    const drawing = link.querySelector("svg");
    if (!(drawing instanceof SVGSVGElement)) {
      throw new Error("Missing native hero drawing");
    }
    const box = drawing.getBoundingClientRect();
    return {
      n: Number(link.getAttribute("data-case")),
      href: link.getAttribute("href"),
      label: link.getAttribute("aria-label"),
      top: box.top,
      left: box.left,
      right: box.right,
      width: box.width,
      height: box.height,
      viewbox: drawing.getAttribute("viewBox"),
    };
  });
  return {
    drawings: rects,
    captions: [...figure.querySelectorAll("figcaption")].map((caption) =>
      caption.textContent?.trim(),
    ),
    popovers: document.querySelectorAll("[data-case-popover]").length,
    center_offset: parent ? (frame.left + frame.right - parent.left - parent.right) / 2 : null,
    inline_margin: parent ? (parent.width - frame.width) / 2 : null,
    width: frame.width,
    cap: Number.parseFloat(getComputedStyle(figure).maxInlineSize),
    overflow: document.documentElement.scrollWidth - window.innerWidth,
  };
};
