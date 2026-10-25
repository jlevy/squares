// Head bootstrap: preserve layout queries and navigation geometry before first paint.
// Embedded documents hide site chrome; non-fragment links leave the preview frame.
(() => {
  const root = document.documentElement;
  // The navigation controller runs after the article. Reserve its collapsed geometry
  // now so a long paper never paints the fully exposed no-script link lists first.
  // With scripts disabled this marker is absent and every navigation link stays visible.
  root.dataset.siteNavEnhanced = "true";
  const query = new URLSearchParams(location.search);
  if (location.pathname.endsWith("/atlas.html")) {
    root.setAttribute("data-site-atlas-view", query.get("atlas") === "grid" ? "grid" : "triangle");
    const scale = query.get("scale");
    root.setAttribute(
      "data-site-atlas-scale",
      scale === "fixed" || scale === "global" ? scale : "row",
    );
  }
  // Either Atlas page honors an explicit size; else a Triangle reached from the top
  // follows the scroll (atlas-view.js) unless the reader asks for reduced motion.
  const size = query.get("size") ?? "";
  if (["small", "medium", "large", "xlarge"].includes(size)) {
    root.setAttribute("data-site-atlas-size", size);
  } else if (
    /\/(atlas\.html|index\.html)?$/.test(location.pathname) &&
    location.hash.length < 2 &&
    query.get("atlas") !== "grid" &&
    query.get("view") !== "embed" &&
    !matchMedia("(prefers-reduced-motion: reduce)").matches
  ) {
    root.setAttribute("data-site-atlas-follow", "");
  }
  if (query.get("view") !== "embed") {
    return;
  }
  root.setAttribute("data-site-view", "embed");
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
