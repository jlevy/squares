// Scroll well into the article, at most 3000px down, without smooth scrolling.
() => {
  const viewport = /** @type {Element} */ (
    document.querySelector("[data-kpress-viewport]") || document.scrollingElement
  );
  viewport.scrollTo({
    top: Math.min(3000, (viewport.scrollHeight - viewport.clientHeight) * 0.6),
    behavior: "instant",
  });
};
