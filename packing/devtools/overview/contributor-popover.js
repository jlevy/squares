// Ordinary contributor links read their canonical page; unmodified presses enhance
// them with the same article in one accessible popover. Each link it enhances says so
// with `aria-haspopup="dialog"`, set here rather than written into every page: on the
// links in the page and in its held templates at start-up, and on those in every
// article the shared loader clones later (`siteArticles.prepare`).
(() => {
  const popover = document.querySelector("[data-contributor-popover]");
  const body = popover?.querySelector("[data-contributor-body]");
  const articles = globalThis.siteArticles;
  if (
    !(popover instanceof HTMLElement) ||
    !(body instanceof HTMLElement) ||
    typeof popover.showPopover !== "function" ||
    articles === undefined
  ) {
    return;
  }
  const action = popover.querySelector("[data-contributor-open]");
  const close = popover.querySelector(".site-popover-close");
  /** @type {HTMLElement | null} */
  let origin = null;
  let latest = 0;

  /**
   * Whether a press on `link` opens the popover rather than following the link.
   * @param {Element | null} link
   * @returns {link is HTMLAnchorElement}
   */
  const enhanced = (link) =>
    link instanceof HTMLAnchorElement &&
    !link.hasAttribute("download") &&
    (link.target === "" || link.target === "_self");

  /** @param {ParentNode} root */
  const announce = (root) => {
    for (const link of root.querySelectorAll("a[data-contributor][href]")) {
      if (enhanced(link)) {
        link.setAttribute("aria-haspopup", "dialog");
      }
    }
    for (const held of root.querySelectorAll("template")) {
      announce(held.content);
    }
  };
  // A page read from a file cannot fetch the article, so its links stay plain links.
  if (/^https?:$/.test(location.protocol)) {
    announce(document);
    articles.prepare(announce);
  }

  // Capture before the source case/result panel's ordinary-link close listener.
  document.addEventListener(
    "click",
    (event) => {
      const link = articles.clickTarget(event)?.closest("a[data-contributor][href]") ?? null;
      if (!enhanced(link)) {
        return;
      }
      event.preventDefault();
      event.stopPropagation();
      const returnTo = articles.returnFocus(link);
      const source = link.closest(".site-popover[popover]");
      const request = ++latest;
      const sharedRequest = articles.beginRequest();
      const href = link.href;
      const current = () =>
        request === latest &&
        articles.isCurrent(sharedRequest) &&
        (source === null || source.matches(":popover-open"));
      void articles.loadArticle(href, "article.site-contributor").then(
        ({ article, responseUrl }) => {
          if (!current()) {
            return;
          }
          origin = returnTo;
          articles.setReturnFocus(popover, origin);
          body.replaceChildren(article);
          const heading = Array.from(article.children).find((child) => child.matches("h1"));
          if (heading instanceof HTMLElement) {
            if (!heading.id) {
              heading.id = `${popover.id}-record-title`;
            }
            popover.setAttribute("aria-labelledby", heading.id);
          }
          action?.setAttribute("href", responseUrl);
          if (!popover.matches(":popover-open")) {
            // Auto popovers nested by DOM/event ancestry can coexist; replacement is explicit.
            if (source instanceof HTMLElement && source !== popover) {
              source.hidePopover();
            }
            popover.showPopover();
          }
          if (close instanceof HTMLElement) {
            close.focus({ preventScroll: true });
          }
          popover.scrollTo({ top: 0, behavior: "instant" });
          body.scrollTo({ top: 0, behavior: "instant" });
        },
        () => {
          if (current()) {
            location.href = href;
          }
        },
      );
    },
    true,
  );

  popover.addEventListener("beforetoggle", (event) => {
    if (event instanceof ToggleEvent && event.newState === "closed") {
      latest += 1;
    }
  });
  popover.addEventListener("toggle", (event) => {
    if (
      !(event instanceof ToggleEvent) ||
      event.newState !== "closed" ||
      origin === null ||
      !origin.isConnected
    ) {
      return;
    }
    const focus = document.activeElement;
    if (focus === null || focus === document.body || popover.contains(focus)) {
      origin.focus();
    }
  });
})();
