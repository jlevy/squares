// The reading text's resolved typography: for the first element of each role inside the
// page's prose column -- a paragraph, h1 to h4, a list item, a table cell, inline code,
// inline math -- its face, size, weight, line height and spacing, and the column's
// measure; with every `--kpress-*` and `--site-*`/`--paper-*` token the column resolves.
() => {
  const column =
    document.querySelector(".kpress-prose") ?? document.querySelector(".kpress") ?? document.body;
  const fontFamily = (/** @type {CSSStyleDeclaration} */ style) =>
    (style.fontFamily.split(",")[0] ?? "").trim().replace(/^["']|["']$/g, "");
  /** @param {string} selector */
  const role = (selector) => {
    const el = [...column.querySelectorAll(selector)].find(
      (node) =>
        !node.closest("nav, figure, .site-nav, .kpress-toc, .hero, .site-hero, .site-card") &&
        node.getClientRects().length > 0,
    );
    if (!el) {
      return null;
    }
    const style = getComputedStyle(el);
    return {
      family: fontFamily(style),
      size: style.fontSize,
      weight: style.fontWeight,
      style: style.fontStyle,
      transform: style.textTransform,
      line_height: style.lineHeight,
      margin: `${style.marginBlockStart} ${style.marginBlockEnd}`,
      box_width: `${Math.round(el.getBoundingClientRect().width)}px`,
      text_width: `${Math.round(
        el.getBoundingClientRect().width -
          parseFloat(style.paddingInlineStart) -
          parseFloat(style.paddingInlineEnd),
      )}px`,
    };
  };
  const tokens = (/** @type {Element} */ el) => {
    const style = getComputedStyle(el);
    /** @type {Record<string, string>} */
    const found = {};
    for (let index = 0; index < style.length; index += 1) {
      const name = style.item(index);
      if (/^--(kpress|site|paper|cert)-/.test(name)) {
        found[name] = style.getPropertyValue(name).trim();
      }
    }
    return found;
  };
  return {
    column: column.className,
    column_width: `${Math.round(column.getBoundingClientRect().width)}px`,
    roles: {
      p: role("p"),
      h1: role("h1"),
      h2: role("h2"),
      h3: role("h3"),
      h4: role("h4"),
      li: role("li"),
      td: role("td"),
      code: role("p code"),
      math: role("p .katex"),
    },
    root_tokens: tokens(document.documentElement),
    column_tokens: tokens(column),
  };
};
