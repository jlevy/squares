// The page is drawn from a `file://` URL, which is what keeps the render offline and
// reproducible, and which turns every relative `href` into a link to the build machine's
// disk. Rewrites each relative anchor against the published site's URL. Anchors only; `img`
// and `link` keep resolving beside the file.
/** @param {string} site */
(site) => {
  for (const a of document.querySelectorAll("a[href]")) {
    const href = a.getAttribute("href");
    if (!href || /^[a-z][a-z0-9+.-]*:/i.test(href) || href.startsWith("#")) {
      continue;
    }
    a.setAttribute("href", new URL(href, site).href);
  }
};
