// The text baselines of the header's labels, from the top of the document in CSS
// pixels: the site's name, every link in the navigation bar, and every section tab. A
// baseline is measured, not inferred from a box's edge: a zero-size inline-block with
// nothing in it sits with its bottom edge on the baseline of the line it is in, so one
// is placed at the end of each label, read, and taken away again. The full or compact
// name is measured according to which label is visible at the current width.
//
// With them: the rule under the bar, and for the current link and the current tab how far
// the baseline stands above the rule (the bar's own, and the foot of the tab strip), which
// is where the current link's underline is drawn from.
// `preview_site.baseline_problems` holds the name and the links to one baseline with it.
() => {
  /** @param {number} value */
  const round = (value) => Math.round(value * 100) / 100;
  /** @param {Element} label */
  const baseline = (label) => {
    const mark = document.createElement("span");
    mark.style.cssText = "display:inline-block;inline-size:0;block-size:0;padding:0;margin:0";
    label.append(mark);
    const y = mark.getBoundingClientRect().bottom + window.scrollY;
    mark.remove();
    return round(y);
  };
  /** @param {Element} el */
  const shown = (el) => el.getClientRects().length > 0;
  /** @param {Element} el */
  const labelled = (el) => ({
    label: (el.textContent ?? "").trim(),
    baseline: baseline(el),
    top: Math.round(el.getBoundingClientRect().top + window.scrollY),
    current: el.getAttribute("aria-current") === "page",
  });
  const nav = document.querySelector(".site-nav");
  const header = document.querySelector(".kpress-site-header");
  const text = [...document.querySelectorAll(".site-nav .site-name-text")].find(shown);
  const tabs = document.querySelector("nav.site-tabs");
  /** @param {Element | null} el */
  const ruled = (el) =>
    el !== null && Number.parseFloat(getComputedStyle(el).borderBottomWidth) > 0;
  const owner = [header, nav].find(ruled) ?? null;
  const rule = owner ? round(owner.getBoundingClientRect().bottom + window.scrollY) : null;
  const links = [...document.querySelectorAll(".site-nav a[data-page]")].map(labelled);
  const strip = tabs ? [...tabs.querySelectorAll("a")].map(labelled) : [];
  const current = links.find((link) => link.current) ?? null;
  const currentTab = strip.find((tab) => tab.current) ?? null;
  return {
    name: text ? baseline(text) : null,
    links,
    tabs: strip,
    rule,
    current_above_rule: current && rule !== null ? round(rule - current.baseline) : null,
    current_tab_above_foot:
      currentTab && tabs
        ? round(tabs.getBoundingClientRect().bottom + window.scrollY - currentTab.baseline)
        : null,
  };
};
