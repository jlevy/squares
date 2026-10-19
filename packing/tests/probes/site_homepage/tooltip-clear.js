// The visible rating explanation's box, every News filter control and site-header
// control it overlaps, and where the header ends while it is shown.
() => {
  const tooltip = document.querySelector(".site-rating-tooltip.kpress-tooltip-visible");
  if (!(tooltip instanceof HTMLElement)) {
    return null;
  }
  const box = tooltip.getBoundingClientRect();
  /** @param {string} selector */
  const covered = (selector) =>
    [...document.querySelectorAll(selector)]
      .filter((control) => {
        const other = control.getBoundingClientRect();
        return (
          other.width > 0 &&
          box.left < other.right &&
          other.left < box.right &&
          box.top < other.bottom &&
          other.top < box.bottom
        );
      })
      .map((control) => control.getAttribute("aria-label") || control.textContent?.trim() || "");
  const header = document.querySelector(".kpress-site-header")?.getBoundingClientRect();
  return {
    box: { x: box.x, y: box.y, width: box.width, height: box.height },
    covers: covered("[data-news-filters] button"),
    covers_header: covered(".kpress-site-header :is(a[href], button)"),
    header_bottom: header ? header.bottom : null,
  };
};
