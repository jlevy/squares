// Ordinary contributor links read their canonical page; unmodified presses enhance
// them with the same article in one accessible popover. A contributor link is known by
// its address, a profile on this site (`profiles/ID.html`), so no page writes a marker
// on each name. Each link it enhances says so with `aria-haspopup="dialog"`, set here
// rather than written into every page: on the links in the page and in its held
// templates at start-up, and on those in every article the shared loader clones later
// (`siteArticles.prepare`).
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

  /** The last step of a profile's path; the directory, `profiles/index.html`, is none. */
  const PROFILE = /\/profiles\/([a-z0-9-]+)\.html$/;
  /**
   * Where a profile link stays a plain link: inside a container that declares its
   * profile links plain (the News and the profile directory), and the panel's own
   * **Open profile** action, which reaches the complete page.
   */
  const PLAIN = "[data-contributor-plain], [data-contributor-open]";
  const site = new URL(document.baseURI).origin;

  /**
   * Whether a press on `link` opens the popover rather than following the link: a link
   * to a profile on this site that neither downloads nor names another target.
   * @param {Element | null} link
   * @returns {link is HTMLAnchorElement}
   */
  const enhanced = (link) => {
    if (
      !(link instanceof HTMLAnchorElement) ||
      link.hasAttribute("download") ||
      !(link.target === "" || link.target === "_self") ||
      link.closest(PLAIN) !== null
    ) {
      return false;
    }
    /** @type {URL} */
    let url;
    try {
      // Against the page, since a held template's own document has no base address.
      url = new URL(link.getAttribute("href") ?? "", document.baseURI);
    } catch {
      return false;
    }
    const id = PROFILE.exec(url.pathname)?.[1];
    if (
      id === undefined ||
      id === "index" ||
      !/^https?:$/.test(url.protocol) ||
      url.origin !== site
    ) {
      return false;
    }
    // A link to the page itself, such as a profile's own in-page anchors, stays one.
    const page = new URL(document.URL);
    page.hash = "";
    url.hash = "";
    return url.href !== page.href;
  };

  /** @param {ParentNode} root */
  const announce = (root) => {
    for (const link of root.querySelectorAll("a[href]")) {
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
      const link = articles.clickTarget(event)?.closest("a[href]") ?? null;
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
