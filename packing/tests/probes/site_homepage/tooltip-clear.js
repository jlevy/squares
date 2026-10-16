// The visible rating explanation's box and every News filter control it overlaps.
() => {
  const tooltip = document.querySelector(".site-rating-tooltip.kpress-tooltip-visible");
  if (!(tooltip instanceof HTMLElement)) {
    return null;
  }
  const box = tooltip.getBoundingClientRect();
  const controls = [...document.querySelectorAll("[data-news-filters] button")];
  return {
    box: { x: box.x, y: box.y, width: box.width, height: box.height },
    covers: controls
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
      .map((control) => control.textContent?.trim() ?? ""),
  };
};
