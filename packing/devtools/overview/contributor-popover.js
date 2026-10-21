// Ordinary contributor links read their canonical page; unmodified presses enhance
// them with the same article in one accessible popover.
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

  // Capture before the source case/result panel's ordinary-link close listener.
  document.addEventListener(
    "click",
    (event) => {
      if (
        event.defaultPrevented ||
        event.button !== 0 ||
        event.metaKey ||
        event.ctrlKey ||
        event.shiftKey ||
        event.altKey ||
        !(event.target instanceof Element)
      ) {
        return;
      }
      const link = event.target.closest("a[data-person][href]");
      if (
        !(link instanceof HTMLAnchorElement) ||
        link.hasAttribute("download") ||
        (link.target !== "" && link.target !== "_self")
      ) {
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
