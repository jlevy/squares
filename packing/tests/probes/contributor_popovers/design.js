/** @param {string} selector */
async (selector) => {
  await document.fonts.ready;
  const article = document.querySelector(selector);
  if (!(article instanceof HTMLElement)) {
    throw new Error("Missing generated contributor article");
  }
  /** @param {Element | null} node */
  const read = (node) => {
    if (node === null) {
      throw new Error("Missing contributor text role");
    }
    const style = getComputedStyle(node);
    return {
      family: style.fontFamily,
      size: Number.parseFloat(style.fontSize),
      weight: Number.parseFloat(style.fontWeight),
      leading: Number.parseFloat(style.lineHeight),
      color: style.color,
      wrap: style.overflowWrap,
      transform: style.textTransform,
    };
  };
  const reference = document.createElement("span");
  reference.style.cssText = "position:absolute;visibility:hidden";
  article.append(reference);
  reference.style.fontSize = "var(--site-font-size-note)";
  reference.style.fontFamily = "var(--kpress-font-sans)";
  reference.style.fontWeight = "var(--site-font-weight-sans-light)";
  reference.style.color = "var(--site-support-color)";
  const note = read(reference);
  reference.style.color = "var(--kpress-doc-text)";
  const foreground = read(reference).color;
  reference.style.color = "var(--site-support-color)";
  reference.style.fontWeight = "var(--site-font-weight-sans-medium)";
  const medium = read(reference).weight;
  const panel = article.closest("[data-contributor-popover]");
  reference.style.fontSize = panel
    ? "calc(var(--kpress-font-size-base) * var(--paper-popover-section-scale))"
    : "var(--kpress-font-size-h2)";
  reference.style.lineHeight = "var(--paper-heading-leading)";
  const section = read(reference);
  reference.style.fontSize =
    "calc(var(--kpress-font-size-base) * var(--paper-popover-title-scale))";
  const headline = read(reference);
  reference.remove();
  const parent = article.parentElement;
  const title = article.querySelector("h1");
  if (title === null) {
    throw new Error("Missing contributor heading");
  }
  const box = article.getBoundingClientRect();
  const panelBox = panel?.getBoundingClientRect();
  const overflow = [article, ...article.querySelectorAll("*")]
    .filter((node) => node instanceof HTMLElement && node.getClientRects().length > 0)
    .filter((node) => {
      const style = getComputedStyle(node);
      return !(
        node.matches(".kpress-math-semantic") &&
        style.position === "absolute" &&
        style.overflow === "hidden" &&
        style.clipPath === "inset(50%)"
      );
    })
    .filter(
      (node) =>
        !(node.matches("article.site-contributor, section") && node.querySelector(".site-wide")),
    )
    .filter((node) => node.scrollWidth > node.clientWidth + 1)
    .map((node) => node.className || node.tagName);
  const breadcrumb = panel ? null : document.querySelector(".site-breadcrumbs");
  return {
    breadcrumbGap: breadcrumb
      ? title.getBoundingClientRect().top - breadcrumb.getBoundingClientRect().bottom
      : null,
    note,
    foreground,
    medium,
    section,
    headline,
    body: read(article.querySelector(".site-contributor-bio") || article),
    title: read(title),
    headings: Array.from(article.querySelectorAll("h2"), read),
    terms: Array.from(article.querySelectorAll("dt"), read),
    notes: Array.from(
      article.querySelectorAll(
        ".site-contributor-breadcrumb, .site-contributor-evidence, " +
          ".site-contributor-identity dd, .site-contributor-links li, " +
          ".site-contributor-credits li, .site-contributor-sources > ol > li",
      ),
      (node) => ({
        ...read(node),
        primary: node.matches(
          ".site-contributor-identity dd, .site-contributor-links li, .site-contributor-credits li",
        ),
      }),
    ),
    overflow,
    wideBounds: Array.from(article.querySelectorAll(".site-wide"), (node) => {
      const rect = node.getBoundingClientRect();
      return { left: rect.left, right: rect.right };
    }),
    pageWidth: document.documentElement.scrollWidth,
    left: panelBox ? box.left - panelBox.left : null,
    right: panelBox ? panelBox.right - box.right : null,
    panelWidth: panelBox?.width,
    bodyClearance: panel && parent ? getComputedStyle(parent).paddingRight : null,
    titleClearance: getComputedStyle(title).paddingRight,
  };
};
