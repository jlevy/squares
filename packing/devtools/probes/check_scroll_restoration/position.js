// The actual scrolling element and its position at one observation: kpress's viewport when
// the page has one, the document's scroller otherwise, with the restoration mode and the
// fragment it was observed under.
() => {
  const viewport = /** @type {Element} */ (
    document.querySelector("[data-kpress-viewport]") || document.scrollingElement
  );
  return {
    top: viewport.scrollTop,
    document_top: scrollY,
    native: viewport === document.scrollingElement,
    restoration: history.scrollRestoration,
    hash: location.hash,
  };
};
