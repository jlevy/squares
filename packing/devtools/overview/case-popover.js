// Case links and frontier rows enhance their native page URLs with one overlay.
// article-loader.js owns fetching, parsing, assets and cloning. This controller owns
// stepping, row expansion, stale-request guards, navigation fallback and return focus.
(() => {
  const popover = document.querySelector("[data-case-popover]");
  const body = popover?.querySelector("[data-case-body]");
  if (
    !(popover instanceof HTMLElement) ||
    !(body instanceof HTMLElement) ||
    typeof popover.showPopover !== "function"
  ) {
    return;
  }
  const action = popover.querySelector("[data-case-open]");
  const frontierAction = popover.querySelector("[data-case-frontier]");
  const atlasAction = popover.querySelector("[data-case-atlas]");
  const expand = popover.querySelector(".site-popover-expand");
  const close = popover.querySelector(".site-popover-close");

  /** What a click on a row leaves alone: the row's own links and controls. */
  const CONTROLS = "a[href], button, input, select, textarea, label, summary";
  /** Where the arrow keys keep their own meaning. */
  const FIELDS = "input, select, textarea";
  const articles = globalThis.siteArticles;
  if (articles === undefined) {
    return;
  }

  /** @param {MouseEvent} event */
  const modified = (event) =>
    event.button !== 0 || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey;

  /**
   * What opened the popover from the page, which focus returns to when it closes.
   * @type {HTMLElement | null}
   */
  let origin = null;
  /**
   * The opener whose record is on its way.
   * @type {HTMLElement | null}
   */
  let asking = null;
  /** The shared request that the pending opener belongs to. */
  let askingRequest = 0;
  /** The number of the latest request: only it may show its record, or navigate. */
  let latest = 0;
  /**
   * The row of the case whose record is shown, which reads as expanded.
   * @type {HTMLTableRowElement | null}
   */
  let expanded = null;

  /**
   * A row reads as expanded while its case's record is shown, however that record was
   * reached: by the row, by a link in it, or by stepping from another case.
   * @param {HTMLElement} article
   */
  const markShown = (article) => {
    const n = article.getAttribute("data-case");
    const row = n === null ? null : document.querySelector(`tr[data-case-row="${n}"]`);
    const shown = row instanceof HTMLTableRowElement ? row : null;
    if (shown !== expanded) {
      expanded?.setAttribute("aria-expanded", "false");
      expanded = shown;
    }
    expanded?.setAttribute("aria-expanded", "true");
  };

  /**
   * Place `article`, the record in the file at `url`, as `opener` asked: a link or a row
   * on the page opens the popover on it, and a step inside the popover replaces the
   * record shown.
   * @param {HTMLElement} article
   * @param {string} url
   * @param {HTMLElement} opener
   */
  const show = (article, url, opener) => {
    const stepping = popover.contains(opener);
    // A step's link goes with the record it is in; a reader who pressed it carries on
    // from the same step in the record that replaces it.
    const held = body.contains(document.activeElement);
    const rel = ["prev", "next"].find((token) => opener.matches(`[rel~="${token}"]`));
    body.replaceChildren(article);
    action?.setAttribute("href", url);
    expand?.setAttribute("href", url);
    const n = article.getAttribute("data-case");
    if (n !== null && /^\d+$/.test(n)) {
      const frontier = new URL("../frontier.html", url);
      frontier.hash = `n-${n}`;
      frontierAction?.setAttribute("href", frontier.href);
      const atlas = new URL("../atlas.html", url);
      atlas.hash = `atlas-n-${n}`;
      atlasAction?.setAttribute("href", atlas.href);
    }
    if (!stepping) {
      origin = articles.returnFocus(opener);
      articles.setReturnFocus(popover, origin);
    }
    markShown(article);
    if (!popover.matches(":popover-open")) {
      const source = opener.closest(".site-popover[popover]");
      if (source instanceof HTMLElement && source !== popover && source.matches(":popover-open")) {
        source.hidePopover();
      }
      popover.showPopover();
      if (close instanceof HTMLElement) {
        close.focus();
      }
    } else if (held) {
      const again = rel ? body.querySelector(`a[data-case-step][rel~="${rel}"]`) : null;
      const next = again instanceof HTMLElement ? again : close;
      if (next instanceof HTMLElement) {
        next.focus({ preventScroll: true });
      }
    }
    popover.scrollTo({ top: 0, behavior: "instant" });
    body.scrollTo({ top: 0, behavior: "instant" });
  };

  /**
   * Fetch the record file at `href` and show its record, or go to the file. A step
   * whose record arrives after the popover has closed is dropped.
   * @param {string} href
   * @param {HTMLElement} opener
   */
  const open = (href, opener) => {
    if (opener === asking && articles.isCurrent(askingRequest)) {
      return;
    }
    const url = new URL(href, document.baseURI);
    url.hash = "";
    latest += 1;
    const request = latest;
    const sharedRequest = articles.beginRequest();
    askingRequest = sharedRequest;
    const sourcePopover = opener.closest(".site-popover[popover]");
    asking = opener;
    const current = () => {
      if (request !== latest || !articles.isCurrent(sharedRequest)) {
        return false;
      }
      asking = null;
      return sourcePopover === null || sourcePopover.matches(":popover-open");
    };
    void articles.loadArticle(url.href, "article.site-case").then(
      ({ article, responseUrl }) => {
        if (current()) {
          show(article, responseUrl, opener);
        }
      },
      () => {
        if (current()) {
          location.href = href;
        }
      },
    );
  };

  // Capture case links before any source overlay's ordinary-link close listener.
  document.addEventListener(
    "click",
    (event) => {
      if (event.defaultPrevented || modified(event) || !(event.target instanceof Element)) {
        return;
      }
      const link = event.target.closest("a[data-case][href]");
      if (!(link instanceof HTMLAnchorElement) || (link.target !== "" && link.target !== "_self")) {
        return;
      }
      event.preventDefault();
      if (link.closest(".site-popover[popover]") !== null) {
        event.stopPropagation();
      }
      open(link.href, link);
    },
    true,
  );

  // A step, or a link to another case, in the record shown loads in place. `popover.js`
  // closes a popover when a link in it is followed, so the click goes no further.
  popover.addEventListener(
    "click",
    (event) => {
      if (event.defaultPrevented || modified(event) || !(event.target instanceof Element)) {
        return;
      }
      const link = event.target.closest("a[data-case-step][href], a[data-case][href]");
      if (!(link instanceof HTMLAnchorElement) || !body.contains(link)) {
        return;
      }
      event.preventDefault();
      event.stopPropagation();
      open(link.href, link);
    },
    true,
  );

  // The arrow keys follow the record's own steps. Focus may be in the popover or, after
  // a press on its text, nowhere; anywhere else on the page, the keys are that place's.
  document.addEventListener("keydown", (event) => {
    if (
      (event.key !== "ArrowLeft" && event.key !== "ArrowRight") ||
      event.defaultPrevented ||
      event.altKey ||
      event.ctrlKey ||
      event.metaKey ||
      event.shiftKey ||
      !popover.matches(":popover-open")
    ) {
      return;
    }
    const target = event.target;
    const nowhere = target === document.body || target === document.documentElement;
    if (
      !(target instanceof Element) ||
      (!nowhere && !popover.contains(target)) ||
      target.closest(FIELDS) !== null ||
      (target instanceof HTMLElement && target.isContentEditable)
    ) {
      return;
    }
    const rel = event.key === "ArrowLeft" ? "prev" : "next";
    const step = body.querySelector(`a[data-case-step][rel~="${rel}"]`);
    if (!(step instanceof HTMLAnchorElement)) {
      return;
    }
    event.preventDefault();
    open(step.href, step);
  });

  popover.addEventListener("beforetoggle", (event) => {
    if (!(event instanceof ToggleEvent) || event.newState !== "closed") {
      return;
    }
    // The native close hides the record before the queued toggle event runs. Clear
    // its row's expanded state synchronously, while the visibility changes with it.
    latest += 1;
    asking = null;
    expanded?.setAttribute("aria-expanded", "false");
    expanded = null;
  });

  popover.addEventListener("toggle", (event) => {
    if (!(event instanceof ToggleEvent) || event.newState !== "closed" || origin === null) {
      return;
    }
    // Back to what opened the popover, unless the reader has already moved on to
    // something else, such as another row whose press closed it.
    const focus = document.activeElement;
    if (
      origin.isConnected &&
      (focus === null || focus === document.body || popover.contains(focus))
    ) {
      origin.focus();
    }
  });

  /**
   * Whether the reader has just selected text in the row, which a click ends.
   * @param {HTMLElement} row
   */
  const selecting = (row) => {
    const selection = document.getSelection();
    return (
      selection !== null &&
      !selection.isCollapsed &&
      selection.anchorNode !== null &&
      row.contains(selection.anchorNode)
    );
  };

  for (const row of document.querySelectorAll("tr[data-case-row][data-case-href]")) {
    const href = row.getAttribute("data-case-href");
    if (!(row instanceof HTMLTableRowElement) || !href) {
      continue;
    }
    row.tabIndex = 0;
    row.setAttribute("aria-expanded", "false");
    if (popover.id) {
      row.setAttribute("aria-controls", popover.id);
    }
    const url = new URL(href, document.baseURI).href;
    row.addEventListener("click", (event) => {
      if (event.defaultPrevented || modified(event) || !(event.target instanceof Element)) {
        return;
      }
      const control = event.target.closest(CONTROLS);
      if ((control !== null && row.contains(control)) || selecting(row)) {
        return;
      }
      event.preventDefault();
      open(url, row);
    });
    row.addEventListener("keydown", (event) => {
      if (
        event.target !== row ||
        (event.key !== "Enter" && event.key !== " ") ||
        event.altKey ||
        event.ctrlKey ||
        event.metaKey
      ) {
        return;
      }
      event.preventDefault();
      open(url, row);
    });
  }
})();
