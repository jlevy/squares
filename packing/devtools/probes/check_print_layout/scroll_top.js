// How far the reader has scrolled: kpress's own viewport when the page has one, the
// document's scrolling element otherwise.
() =>
  /** @type {Element} */ (
    document.querySelector("[data-kpress-viewport]") || document.scrollingElement
  ).scrollTop;
