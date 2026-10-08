// Input response: every link to a case record on a page that carries the case popover opens it there: an
// atlas tile on the overview, the `n` of a frontier row, a link in the page's prose or in
// a record, each an `a[data-case]` whose `href` is the record file, `cases/11.html`
// (`render_case_pages.mark_case_links`). A result's overview links its cases as pages. A
// frontier row, `tr[data-case-row]`, is one control for its case as a results row is for
// its detail (`row-popover.js`): it takes focus, and a click anywhere on it but on its
// own links and controls, or Enter or Space while it has focus, opens the record file it
// names in `data-case-href`; the row of the case shown reads as expanded. Without this
// script every link goes to the record file, which sends a reader on to the record page.
//
// The record is fetched, not framed. The file holds the record alone, as HTML, in
// `article.site-case`; it is parsed in a `<template>`, so none of its scripts runs (one
// would send this page away), and the article is placed in the popover's body
// (`[data-case-body]`), with the action under it (`[data-case-open]`) pointed at the
// file. The file's links are written from its own directory, so every relative `href`
// and `src` in the record is resolved against the file's address first; a bare fragment
// names a place in the record and is kept. Each file is fetched once a page. A fetch that
// fails, as every fetch does on a page read from a file, sends the reader to the record
// file itself, as the link would have.
//
// The record's steps (`a[data-case-step]`), and the left and right arrow keys while the
// popover is open and no form control has focus, load the neighbouring case in the same
// popover at its top; the record's link to every case (`a[data-case-index]`) is an
// ordinary link. A press on what is already being fetched waits for it. Closing returns
// focus to what opened the popover, if focus has been lost.
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
  const close = popover.querySelector(".site-popover-close");

  /** What a click on a row leaves alone: the row's own links and controls. */
  const CONTROLS = "a[href], button, input, select, textarea, label, summary";
  /** Where the arrow keys keep their own meaning. */
  const FIELDS = "input, select, textarea";
  /** A value that begins with a scheme, `https:`, `mailto:` or `data:`, is absolute. */
  const SCHEME = /^[a-z][a-z\d+.-]*:/i;

  /**
   * Whether a click asks for something other than following a link here: another
   * button, or a modifier that opens it in a tab or a window.
   * @param {MouseEvent} event
   */
  const modified = (event) =>
    event.button !== 0 || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey;

  /**
   * Resolve every relative `href` and `src` under `root` against `base`, the address of
   * the file the markup was written for.
   * @param {Element} root
   * @param {string} base
   */
  const rebase = (root, base) => {
    for (const node of root.querySelectorAll("[href], [src]")) {
      for (const name of ["href", "src"]) {
        const value = node.getAttribute(name)?.trim();
        if (value === undefined || value.startsWith("#") || SCHEME.test(value)) {
          continue;
        }
        try {
          node.setAttribute(name, new URL(value, base).href);
        } catch {
          // A value no address can be made of is left as it was written.
        }
      }
    }
  };

  /**
   * The record in the file at `url`, its links resolved.
   * @param {string} url
   * @returns {Promise<HTMLElement>}
   */
  const fetchRecord = async (url) => {
    if (location.protocol === "file:") {
      throw new Error("a page read from a file cannot fetch a record");
    }
    const response = await fetch(url);
    if (!response.ok) {
      throw new Error(`${url}: ${response.status}`);
    }
    const parsed = document.createElement("template");
    parsed.innerHTML = await response.text();
    const article = parsed.content.querySelector("article.site-case");
    if (!(article instanceof HTMLElement)) {
      throw new Error(`${url} holds no case record`);
    }
    rebase(article, response.url || url);
    return article;
  };

  /**
   * Each record asked for, by its file's address. The article itself is kept, so a
   * record shown again keeps its typeset math; a failure is dropped, so the next press
   * asks again.
   * @type {Map<string, Promise<HTMLElement>>}
   */
  const records = new Map();
  /** @param {string} url */
  const record = (url) => {
    let held = records.get(url);
    if (held === undefined) {
      held = fetchRecord(url);
      records.set(url, held);
      void held.catch(() => {
        records.delete(url);
      });
    }
    return held;
  };

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
    if (!stepping) {
      origin = opener;
    }
    markShown(article);
    if (!popover.matches(":popover-open")) {
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
    if (opener === asking) {
      return;
    }
    const url = new URL(href, document.baseURI);
    url.hash = "";
    latest += 1;
    const request = latest;
    asking = opener;
    const current = () => {
      if (request !== latest) {
        return false;
      }
      asking = null;
      return !popover.contains(opener) || popover.matches(":popover-open");
    };
    void record(url.href).then(
      (article) => {
        if (current()) {
          show(article, url.href, opener);
        }
      },
      () => {
        if (current()) {
          location.href = href;
        }
      },
    );
  };

  // Any link to a case on the page. A link in the popover's record is caught below,
  // before it gets here.
  document.addEventListener("click", (event) => {
    if (event.defaultPrevented || modified(event) || !(event.target instanceof Element)) {
      return;
    }
    const link = event.target.closest("a[data-case][href]");
    if (!(link instanceof HTMLAnchorElement) || (link.target !== "" && link.target !== "_self")) {
      return;
    }
    event.preventDefault();
    open(link.href, link);
  });

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
    if (focus === null || focus === document.body || popover.contains(focus)) {
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
