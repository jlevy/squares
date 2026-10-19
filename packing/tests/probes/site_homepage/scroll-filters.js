// Scroll so the News filters' top edge stands `offset` pixels below the window's top,
// and return where it stands.
(/** @type {number} */ offset) => {
  const filters = document.querySelector("[data-news-filters]");
  if (!(filters instanceof HTMLElement)) {
    return null;
  }
  window.scrollBy(0, filters.getBoundingClientRect().top - offset);
  return filters.getBoundingClientRect().top;
};
