// Where a page's header stands, from the top of the document in CSS pixels: the
// navigation bar, the rule under it, the section tabs a page of a section carries (the
// Visualize section's Film and Workbench) and the first block of the page's content.
// The rule is the lower border of the header slot, or of the bar where the slot hands
// its rule to the bar; the first block is an application's viewport, or whatever opens
// a page's column, a title, a picture or a table, passing over what is out of the flow.
// `preview_site.tabs_problems` holds the tabs to their place below the rule with it.
//
// With them, the header's type: the computed font size of the site's name, of a link in
// the bar and of a section tab, beside the body's, a prose paragraph's where the page has
// one, and the paper's scale as this page resolves it (the prose base, the sans base and
// the support, note and colophon steps under it), each step set on a probe element and
// read back; it is null on a page that does not carry the scale's tokens, as the
// optimality paper does not. `links_rows` is how many lines the bar's links take and `overflow` how far
// the page runs past the window. `preview_site.type_problems` holds the bar's type to the
// body's with it.
() => {
  /** @param {number} value */
  const round = (value) => Math.round(value * 100) / 100;
  /** @param {Element} el */
  const box = (el) => {
    const rect = el.getBoundingClientRect();
    return {
      top: round(rect.top + window.scrollY),
      bottom: round(rect.bottom + window.scrollY),
      left: round(rect.left),
      right: round(rect.right),
    };
  };
  /** @param {Element} el */
  const name = (el) =>
    [
      el.tagName.toLowerCase() + (el.id ? `#${el.id}` : ""),
      ...[...el.classList].filter((item) => !item.startsWith("kpress-")),
    ]
      .join(".")
      .slice(0, 60);
  /** @param {Element} el */
  const inFlow = (el) => {
    if (el.getClientRects().length === 0 || el.matches("script, style, template")) {
      return false;
    }
    const position = getComputedStyle(el).position;
    return position !== "absolute" && position !== "fixed" && el.getBoundingClientRect().height > 0;
  };
  const nav = document.querySelector(".site-nav");
  const header = document.querySelector(".kpress-site-header");
  // Section navigation belongs to the header; a page can also carry an inline
  // Visuals chooser or an atlas tablist inside its reading column.
  const tabs = header?.querySelector("nav.site-tabs") ?? null;
  /** @param {Element | null} el */
  const ruled = (el) =>
    el !== null && Number.parseFloat(getComputedStyle(el).borderBottomWidth) > 0;
  const owner = [header, nav].find(ruled) ?? null;
  let rule = null;
  if (owner) {
    const edge = box(owner);
    const width = Number.parseFloat(getComputedStyle(owner).borderBottomWidth);
    rule = { ...edge, top: round(edge.bottom - width), on: name(owner) };
  }
  /** @type {Element | null} */
  let first = document.querySelector("#viewport, .kpress-long-text, .cert-page");
  while (first && !first.matches("#viewport") && first.matches("div, header, section, article")) {
    const child = [...first.children].find(inFlow);
    if (!child) {
      break;
    }
    first = child;
  }
  /** @param {Element | null} el */
  const size = (el) => (el ? round(Number.parseFloat(getComputedStyle(el).fontSize)) : null);
  const probe = document.createElement("span");
  document.documentElement.append(probe);
  /** @param {string} expression */
  const step = (expression) => {
    probe.style.fontSize = expression;
    return size(probe);
  };
  const prose = "var(--kpress-host-font-size-base)";
  const sans = `calc(${prose} * var(--paper-font-scale-sans))`;
  const carried = getComputedStyle(document.documentElement).getPropertyValue(
    "--paper-font-scale-sans",
  );
  const scale = carried.trim()
    ? {
        prose: step(prose),
        sans: step(sans),
        support: step(`calc(${sans} * var(--paper-support-scale))`),
        note: step(`calc(${sans} * var(--paper-note-scale))`),
        colophon: step(`calc(${sans} * var(--paper-colophon-scale))`),
      }
    : null;
  probe.remove();
  const links = [...document.querySelectorAll(".site-nav a[data-page]")];
  const lines = new Set(links.map((link) => Math.round(link.getBoundingClientRect().top)));
  const nameText = [...document.querySelectorAll(".site-nav .site-name-text")].find(
    (label) => label.getClientRects().length > 0,
  );
  return {
    nav: nav && box(nav),
    type: {
      body: size(document.querySelector(".kpress-long-text > p:not([class])")),
      name: size(document.querySelector(".site-nav .site-name")),
      name_shown: nameText !== undefined,
      name_label: nameText?.textContent ?? null,
      link: size(links[0] ?? null),
      tab: size(tabs?.querySelector("a") ?? null),
      tab_scale:
        Number.parseFloat(
          getComputedStyle(document.documentElement).getPropertyValue("--paper-button-label-scale"),
        ) || 1,
      links_rows: lines.size,
      overflow: document.documentElement.scrollWidth - document.documentElement.clientWidth,
      scale,
    },
    rule,
    tabs: tabs && {
      ...box(tabs),
      current: tabs.querySelector('[aria-current="page"]')?.textContent ?? null,
    },
    first: first && { ...box(first), block: name(first) },
  };
};
