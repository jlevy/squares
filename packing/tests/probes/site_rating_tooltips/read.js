/** @param {string} selector */
async (selector) => {
  await document.fonts.ready;
  const trigger = document.querySelector(selector);
  const id = trigger?.getAttribute("aria-describedby")?.split(/\s+/).at(-1);
  const tooltip = id ? document.getElementById(id) : null;
  const rect = tooltip?.getBoundingClientRect();
  const style = tooltip ? getComputedStyle(tooltip) : null;
  return {
    name: trigger?.getAttribute("aria-label"),
    title: trigger?.getAttribute("title"),
    role: trigger?.getAttribute("role"),
    tab: trigger?.getAttribute("tabindex"),
    focused: document.activeElement === trigger,
    described: tooltip?.getAttribute("role") === "tooltip",
    text: tooltip?.textContent,
    active: document.querySelectorAll(".site-rating-tooltip.kpress-tooltip-visible").length,
    top_layer: tooltip?.matches(":popover-open"),
    unclipped:
      rect &&
      tooltip === document.elementFromPoint(rect.left + rect.width / 2, rect.top + rect.height / 2),
    left: rect?.left,
    right: rect?.right,
    top: rect?.top,
    bottom: rect?.bottom,
    width: document.documentElement.clientWidth,
    height: window.innerHeight,
    transition: style?.transitionDuration,
    background: style?.backgroundColor,
    family: style?.fontFamily,
    opacity: style?.opacity,
    native_titles: document.querySelectorAll(
      ".site-atlas-badge[title], .site-significance[title], .site-chip.site-rung-fill[title], .site-star[title], .badge-item[title]",
    ).length,
    names: [...document.querySelectorAll("[data-site-tooltip]")].map((badge) =>
      badge.getAttribute("aria-label"),
    ),
  };
};
