// Protocol-aware first-screen font preloads: choose credentials before activation.
// WebKit rejects anonymous file-origin preloads and poisons the CSS font cache.
() => {
  const protocol = location.protocol;
  if (!["http:", "https:", "file:"].includes(protocol)) {
    return;
  }
  for (const link of document.querySelectorAll("link[data-site-font-preload]")) {
    const hint = /** @type {HTMLLinkElement} */ (link);
    if (
      !/^(?:\.\.\/)*assets\/fonts\/[a-z0-9-]+\.[0-9a-f]{16}\.woff2$/.test(
        hint.getAttribute("href") || "",
      )
    ) {
      continue;
    }
    if (protocol !== "file:") {
      hint.crossOrigin = "anonymous";
    }
    hint.rel = "preload";
  }
};
