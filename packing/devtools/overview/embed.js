// Head bootstrap: preserve whitelisted layout queries before the body is painted.
// A site page shown inside another page's popover. The overview's cards open their
// target in a narrow frame with `?view=embed`; such a page drops its site chrome (the
// navigation bar) so only the document shows, and a link out of it opens in the whole
// window, so following one leaves the preview for the full page rather than navigating
// inside the frame. A link to a place on the same page still scrolls the frame.
// Runs in the head, before the body is drawn, so the chrome never flashes.
(() => {
  const query = new URLSearchParams(location.search);
  document.documentElement.setAttribute(
    "data-site-atlas-view",
    query.get("atlas") === "grid" ? "grid" : "triangle",
  );
  const size = query.get("size");
  document.documentElement.setAttribute(
    "data-site-atlas-size",
    size === "medium" || size === "large" ? size : "small",
  );
  const scale = query.get("scale");
  document.documentElement.setAttribute(
    "data-site-atlas-scale",
    scale === "row" || scale === "global" ? scale : "fixed",
  );
  if (query.get("view") !== "embed") {
    return;
  }
  document.documentElement.setAttribute("data-site-view", "embed");
  document.addEventListener(
    "click",
    (event) => {
      const link = event.target instanceof Element ? event.target.closest("a[href]") : null;
      if (!(link instanceof HTMLAnchorElement) || link.getAttribute("href")?.startsWith("#")) {
        return;
      }
      link.target = "_top";
    },
    true,
  );
})();
