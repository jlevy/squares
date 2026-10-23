// Measure actual page families, separating padded card interiors from prose edges.
async () => {
  await document.fonts.ready;
  /** @param {Element} element */
  const box = (element) => {
    const rect = element.getBoundingClientRect();
    const style = getComputedStyle(element);
    const inset =
      Number.parseFloat(style.paddingInlineStart) +
      Number.parseFloat(style.paddingInlineEnd) +
      Number.parseFloat(style.borderInlineStartWidth) +
      Number.parseFloat(style.borderInlineEndWidth);
    return {
      element: `${element.tagName.toLowerCase()}.${element.className}`,
      left: rect.left,
      right: rect.right,
      width: rect.width,
      content: rect.width - inset,
      inset,
      max: style.maxInlineSize,
      font: style.fontSize,
    };
  };
  /** @param {Element} element */
  const visible = (element) => element.getClientRects().length > 0;
  const root = document.querySelector(".site-page") ?? document.querySelector(".cert-page");
  if (!root) {
    throw new Error("This page has no standard prose shell");
  }
  const paragraphs = [...root.querySelectorAll("p")]
    .filter(visible)
    .filter(
      (element) =>
        element.textContent?.trim() &&
        !element.closest(
          "nav, figure, table, li, blockquote, .site-card, .site-hero, .site-popover, .site-colophon, .colophon, .site-news-metadata, .site-article-header, .site-action-row",
        ),
    )
    .map((element) => {
      const surface = element.closest(".site-news-day, .boxed-text, details");
      return {
        ...box(element),
        text: element.textContent?.trim().slice(0, 70),
        parent: element.parentElement?.className,
        card: surface ? box(surface) : null,
      };
    });
  const brand = [...document.querySelectorAll(".site-name-text")].find(visible);
  const firstTrail = document.querySelector(".site-breadcrumbs li");
  return {
    viewport: innerWidth,
    root: box(root),
    brand: brand ? box(brand) : null,
    firstTrail: firstTrail ? box(firstTrail) : null,
    wrappers: [
      ...document.querySelectorAll(
        ".kpress-doc, .kpress-long-text, .site-contributor, .site-contributor-directory, .site-breadcrumbs",
      ),
    ]
      .filter(visible)
      .map(box),
    paragraphs,
    cards: [...root.querySelectorAll(".site-cards-frame")].filter(visible).map(box),
    cardBodies: [...root.querySelectorAll(".site-card")].filter(visible).map(box),
    news: [...root.querySelectorAll(".site-news-day")].filter(visible).slice(0, 3).map(box),
    wide: [...root.querySelectorAll(".site-wide, .site-table-wrap")]
      .filter(visible)
      .slice(0, 5)
      .map(box),
    overflow: document.documentElement.scrollWidth - document.documentElement.clientWidth,
  };
};
