// Head bootstrap: preserve layout queries and navigation geometry before first paint.
// Embedded documents hide site chrome; non-fragment links leave the preview frame.
(() => {
  // The navigation controller runs after the article. Reserve its collapsed geometry
  // now so a long paper never paints the fully exposed no-script link lists first.
  // With scripts disabled this marker is absent and every navigation link stays visible.
  document.documentElement.dataset.siteNavEnhanced = "true";
  const query = new URLSearchParams(location.search);
  if (location.pathname.endsWith("/atlas.html")) {
    document.documentElement.setAttribute(
      "data-site-atlas-view",
      query.get("atlas") === "grid" ? "grid" : "triangle",
    );
    const scale = query.get("scale");
    document.documentElement.setAttribute(
      "data-site-atlas-scale",
      scale === "fixed" || scale === "global" ? scale : "row",
    );
  }
  // Both the dedicated Atlas and the homepage preview honor an explicit size.
  // An absent or invalid choice leaves the CSS viewport default in control.
  const size = query.get("size");
  const named = size === "small" || size === "medium" || size === "large";
  if (named) {
    document.documentElement.setAttribute("data-site-atlas-size", size);
  }
  // A Triangle reached from the top of either Atlas page follows the scroll, so it
  // opens at Large (atlas-view.js). A fragment, a size, Grid or an embedding each
  // open where they always did.
  const grid = location.pathname.endsWith("/atlas.html") && query.get("atlas") === "grid";
  if (
    /\/(atlas\.html|index\.html)?$/.test(location.pathname) &&
    location.hash.length < 2 &&
    !named &&
    !grid &&
    query.get("view") !== "embed"
  ) {
    document.documentElement.setAttribute("data-site-atlas-follow", "");
  }
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
