// The white space around every table and every heading as laid out, and each heading's
// leading. A gap is measured between border boxes, so it is what a reader sees whatever
// margins, padding and collapsing made it: from the box above to the top of the block,
// and from its foot to the box below. The box above or below is the nearest one in the
// flow, found by walking the siblings and then the ancestors' siblings; a closed popover,
// a contents rail and anything out of the flow is passed over. Where a block is the first
// or last thing in its frame (a popover, a card, the page), the gap is to the frame's
// inner edge and `to` says so.
//
// A table is measured as the component a reader sees: its filter bar, when it has one,
// the legend under the bar where it has one, and its wrap; a table inside a disclosure is measured as the disclosure, open or
// closed, with the space inside it reported apart. Beside the space above and below it,
// a table has its side gutters: how far its wrap, and its bar's, sit from the edges of
// the window, or of the popover that holds it. A grid marked up with a table's roles, as
// a result overview's are, is measured as a table. A heading is every `h1` to `h4` and
// every headline set in a heading's face: a card's, a popover's, a case record's.
// The page's first block is whatever opens its column, a title, a picture or a row of
// chips, with the space from the bar's rule down to it.
// `scope` keeps only what sits inside an element it matches, for what a press opened.
(/** @type {{scope?: string | null} | undefined} */ options) => {
  const scope = options?.scope ?? null;
  /** @param {number} value */
  const round = (value) => Math.round(value * 10) / 10;
  /** @param {Element} el */
  const shown = (el) => el.getClientRects().length > 0;
  /** @param {Element} el */
  const inFlow = (el) => {
    if (!shown(el) || el.matches(".kpress-toc, script, style, template")) {
      return false;
    }
    const style = getComputedStyle(el);
    return (
      style.position !== "absolute" &&
      style.position !== "fixed" &&
      el.getBoundingClientRect().height > 0
    );
  };
  const frames = "body, [popover], .site-card, td, th";
  /** @param {Element} el */
  const name = (el) =>
    [el.tagName.toLowerCase(), ...[...el.classList].filter((item) => !item.startsWith("kpress-"))]
      .join(".")
      .slice(0, 60);
  /**
   * @param {Element} el
   * @param {"previousElementSibling" | "nextElementSibling"} step
   * @returns {{gap: number, to: string}}
   */
  const gap = (el, step) => {
    const box = el.getBoundingClientRect();
    const above = step === "previousElementSibling";
    /** @type {Element} */
    let at = el;
    while (!at.matches(frames)) {
      for (let sibling = at[step]; sibling; sibling = sibling[step]) {
        if (inFlow(sibling)) {
          const other = sibling.getBoundingClientRect();
          return {
            gap: round(above ? box.top - other.bottom : other.top - box.bottom),
            to: name(sibling),
          };
        }
      }
      if (!at.parentElement) {
        break;
      }
      at = at.parentElement;
    }
    const frame = at.getBoundingClientRect();
    const style = getComputedStyle(at);
    const inner = above
      ? frame.top + parseFloat(style.borderTopWidth) + parseFloat(style.paddingTop)
      : frame.bottom - parseFloat(style.borderBottomWidth) - parseFloat(style.paddingBottom);
    return {
      gap: round(above ? box.top - inner : inner - box.bottom),
      to: `edge of ${name(at)}`,
    };
  };
  const headings = [...document.querySelectorAll("h2")];
  /** @param {Element} block */
  const section = (block) => {
    const before = headings.filter(
      (heading) =>
        heading !== block &&
        heading.compareDocumentPosition(block) & Node.DOCUMENT_POSITION_FOLLOWING,
    );
    return (before.at(-1)?.textContent ?? "").trim();
  };
  /** @param {Element} el */
  const kept = (el) => scope === null || el.closest(scope) !== null;

  /** @type {Set<Element>} */
  const seen = new Set();
  const tables = [];
  /**
   * How far a box sits inside its frame's side edges: the window's, or the border box of
   * the popover that holds it.
   * @param {Element} el
   */
  const sides = (el) => {
    const box = el.getBoundingClientRect();
    const frame = el.closest("[popover]")?.getBoundingClientRect() ?? null;
    return {
      left: round(box.left - (frame?.left ?? 0)),
      right: round((frame?.right ?? document.documentElement.clientWidth) - box.right),
    };
  };
  /** @param {Element} el */
  const scrollsSideways = (el) => getComputedStyle(el).overflowX !== "visible";
  for (const table of document.querySelectorAll('table, [role="table"]')) {
    const wrap =
      table.closest(".site-table-wrap") ??
      table.closest(".kpress-table-wrap") ??
      table.closest(".site-result-case-list") ??
      table;
    const held = wrap.closest("[popover]") !== null;
    const disclosure = held ? null : wrap.closest("details");
    const component = disclosure ?? wrap;
    if (seen.has(component) || !shown(component) || !kept(component)) {
      continue;
    }
    if (table.closest("nav, .kpress-toc")) {
      continue;
    }
    seen.add(component);
    // A table of results sets its legend between its bar and its wrap
    // (`overview_sections.rung_legend`): the bar is the one above the legend.
    let before = disclosure ? null : wrap.previousElementSibling;
    while (before?.classList.contains("site-rung-legend")) {
      before = before.previousElementSibling;
    }
    const bar =
      before instanceof Element && before.matches(".site-table-tools") && shown(before)
        ? before
        : null;
    const top = bar ?? component;
    const above = gap(top, "previousElementSibling");
    const below = gap(component, "nextElementSibling");
    const summary = disclosure?.querySelector(":scope > summary") ?? null;
    const open = disclosure ? disclosure.open && shown(wrap) : null;
    tables.push({
      table: name(table),
      section: section(component),
      component: name(component),
      open,
      bar: bar !== null,
      above: above.gap,
      above_to: above.to,
      bar_to_table: bar
        ? round(wrap.getBoundingClientRect().top - bar.getBoundingClientRect().bottom)
        : null,
      summary_to_table:
        open && summary
          ? round(wrap.getBoundingClientRect().top - summary.getBoundingClientRect().bottom)
          : null,
      below: below.gap,
      below_to: below.to,
      ...sides(disclosure && !open ? disclosure : wrap),
      sides_to: held ? "popover" : "window",
      bar_left: bar ? sides(bar).left : null,
      bar_right: bar ? sides(bar).right : null,
      // Content wider than the wrap either scrolls inside it or, where the wrap does not
      // clip, spills out of it by this many pixels.
      scrolls: wrap.scrollWidth > wrap.clientWidth + 1 && scrollsSideways(wrap),
      spills:
        wrap.scrollWidth > wrap.clientWidth + 1 && !scrollsSideways(wrap)
          ? wrap.scrollWidth - wrap.clientWidth
          : 0,
      top: Math.round(top.getBoundingClientRect().top + window.scrollY),
    });
  }

  const roles =
    "h1, h2, h3, h4, .site-card-value, .site-popover-value, .site-case-title, .subtitle";
  const found = [];
  for (const el of document.querySelectorAll(roles)) {
    if (!shown(el) || !kept(el) || el.closest("nav, .kpress-toc")) {
      continue;
    }
    const style = getComputedStyle(el);
    const box = el.getBoundingClientRect();
    const size = parseFloat(style.fontSize);
    const leading = parseFloat(style.lineHeight);
    const inner =
      box.height -
      parseFloat(style.paddingTop) -
      parseFloat(style.paddingBottom) -
      parseFloat(style.borderTopWidth) -
      parseFloat(style.borderBottomWidth);
    const above = gap(el, "previousElementSibling");
    const below = gap(el, "nextElementSibling");
    found.push({
      role: name(el),
      text: (el.textContent ?? "").trim().replace(/\s+/g, " ").slice(0, 48),
      size: round(size),
      line_height: Number.isNaN(leading) ? style.lineHeight : round(leading),
      leading: Number.isNaN(leading) ? null : Math.round((leading / size) * 1000) / 1000,
      lines: Number.isNaN(leading) ? null : Math.round(inner / leading),
      height: round(inner),
      // What the box cannot show of its own content: above zero, a box that hides its
      // overflow is clipping its text or a formula in it.
      overflow: Math.max(0, el.scrollHeight - el.clientHeight),
      clips: style.overflowY !== "visible",
      math: el.querySelector(".kpress-math, .katex, .tex") !== null,
      margin: `${style.marginTop} ${style.marginBottom}`,
      above: above.gap,
      above_to: above.to,
      below: below.gap,
      below_to: below.to,
      top: Math.round(box.top + window.scrollY),
    });
  }
  // The first block: down through the column's wrappers to the first thing a reader sees.
  const firsts = [];
  /** @type {Element | null} */
  let first = scope === null ? document.querySelector(".kpress-long-text, .cert-page") : null;
  while (first?.matches("div, header, section, article")) {
    const child = [...first.children].find(inFlow);
    if (!child) {
      break;
    }
    first = child;
  }
  if (first) {
    const above = gap(first, "previousElementSibling");
    firsts.push({ block: name(first), above: above.gap, above_to: above.to });
  }
  return { tables, headings: found, first: firsts };
};
