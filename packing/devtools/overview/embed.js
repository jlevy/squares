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
  // Either Atlas page honors an explicit size; else the stylesheet's default holds, or
  // a Triangle reached from the top follows the scroll (atlas-view.js).
  const size = query.get("size") ?? "";
  const named = ["small", "medium", "large", "xlarge"].includes(size);
  if (named) {
    document.documentElement.setAttribute("data-site-atlas-size", size);
  } else if (
    /\/(atlas\.html|index\.html)?$/.test(location.pathname) &&
    location.hash.length < 2 &&
    query.get("atlas") !== "grid" &&
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
