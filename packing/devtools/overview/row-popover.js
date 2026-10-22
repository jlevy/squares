// Input response: table rows open a detail overlay. Ordinary result links also open
// the complete canonical page without JavaScript. On the first opening, the overlay
// fetches that page, extracts its prepared article and resolves relative links against
// the response URL. Sorting and filtering preserve each row's named overlay.
(() => {
  const available = globalThis.siteArticles;
  if (available === undefined) {
    return;
  }
  const articles = available;
  /** @type {WeakMap<HTMLElement, number>} */
  const generations = new WeakMap();

  /** What a click on a row leaves alone: the row's own links and controls. */
  const CONTROLS = "a[href], button, input, select, textarea, label, summary";

  /**
   * The popover a row names, if it is on the page and the browser has popovers.
   * @param {HTMLElement} row
   * @returns {HTMLElement | null}
   */
  function popoverOf(row) {
    const id = row.getAttribute("data-row-popover");
    const popover = id ? document.getElementById(id) : null;
    return popover instanceof HTMLElement && typeof popover.showPopover === "function"
      ? popover
      : null;
  }

  /**
   * Fetch each fuller body `popover` names and put it in place of the short one.
   * @param {HTMLElement} popover
   */
  function fetchBodies(popover) {
    if (location.protocol === "file:") {
      return;
    }
    for (const body of popover.querySelectorAll("[data-row-pop-src]")) {
      const source = body.getAttribute("data-row-pop-src");
      if (!(body instanceof HTMLElement) || !source || body.hasAttribute("data-row-pop-loading")) {
        continue;
      }
      body.setAttribute("data-row-pop-loading", "");
      const generation = generations.get(popover) || 0;
      void articles
        .loadArticle(source, "article.site-result[data-result-overview]")
        .then(({ article }) => {
          if (generation !== (generations.get(popover) || 0)) {
            return;
          }
          const heading = Array.from(article.children).find((child) => child.matches("h1"));
          body.replaceChildren(article);
          if (heading instanceof HTMLElement) {
            // The shared loader scopes this clone's heading and every local reference.
            if (!heading.id) {
              heading.id = `${popover.id}-record-title`;
            }
            popover.setAttribute("aria-labelledby", heading.id);
            // The short title stays usable while loading or offline. Once the full
            // title is present it owns the dialog's name, without repeating above it.
            for (const outer of [...popover.children]) {
              if (outer.matches(".site-card-label, .site-popover-value")) {
                outer.remove();
              }
            }
          }
          body.removeAttribute("data-row-pop-src");
        })
        // The short body is already there; a later opening tries again.
        .catch(() => undefined)
        .finally(() => {
          if (generation === (generations.get(popover) || 0)) {
            body.removeAttribute("data-row-pop-loading");
          }
        });
    }
  }

  /**
   * Whether the reader has just selected text in the row, which a click ends.
   * @param {HTMLElement} row
   * @returns {boolean}
   */
  function selecting(row) {
    const selection = document.getSelection();
    return (
      selection !== null &&
      !selection.isCollapsed &&
      selection.anchorNode !== null &&
      row.contains(selection.anchorNode)
    );
  }

  /**
   * Make one row the control for its popover. Safe to call twice.
   * @param {HTMLElement} row
   */
  function wire(row) {
    const popover = popoverOf(row);
    if (popover === null || row.hasAttribute("data-row-ready")) {
      return;
    }
    row.setAttribute("data-row-ready", "");
    row.tabIndex = 0;
    row.setAttribute("aria-expanded", "false");
    row.setAttribute("aria-controls", popover.id);
    for (const trigger of row.querySelectorAll("[popovertarget]")) {
      if (trigger instanceof HTMLElement) {
        trigger.tabIndex = -1;
      }
    }

    const open = () => {
      if (popover.matches(":popover-open")) {
        return;
      }
      articles.cancelRequests();
      articles.setReturnFocus(popover, row);
      popover.showPopover();
      // The toggle event below says the same a task later; the row's wash should not wait.
      row.setAttribute("aria-expanded", "true");
      const close = popover.querySelector(".site-popover-close");
      if (close instanceof HTMLElement) {
        close.focus();
      }
    };

    /**
     * Whether a press or click landed on one of the row's own links or controls, other
     * than its popover's trigger, and so is that control's and not the row's.
     * @param {Element} target
     */
    const ownControl = (target) => {
      const control = target.closest(CONTROLS);
      return (
        control !== null &&
        row.contains(control) &&
        control.getAttribute("popovertarget") !== popover.id
      );
    };

    // A press starts the fetch a moment before the click that opens the popover. A press
    // the click will leave alone, such as on a name linking to a profile, fetches nothing.
    row.addEventListener("pointerdown", (event) => {
      const target = articles.clickTarget(event);
      if (target !== null && !ownControl(target)) {
        fetchBodies(popover);
      }
    });

    row.addEventListener("click", (event) => {
      const target = articles.clickTarget(event);
      if (target === null || ownControl(target) || selecting(row)) {
        return;
      }
      // The trigger opens its popover natively too; cancelling the click leaves one
      // path, this one, so focus moves the same way however the row was pressed.
      event.preventDefault();
      open();
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
      open();
    });

    // A body held in a template is placed before the popover shows, so it is there for
    // the first paint and for the math pass the open popover gets.
    popover.addEventListener("beforetoggle", (event) => {
      if (!(event instanceof ToggleEvent)) {
        return;
      }
      if (event.newState === "closed") {
        generations.set(popover, (generations.get(popover) || 0) + 1);
        row.setAttribute("aria-expanded", "false");
        for (const pending of popover.querySelectorAll("[data-row-pop-loading]")) {
          pending.removeAttribute("data-row-pop-loading");
        }
        return;
      }
      articles.setReturnFocus(popover, row);
      for (const held of popover.querySelectorAll("template[data-row-pop-body]")) {
        if (held instanceof HTMLTemplateElement) {
          held.replaceWith(held.content);
        }
      }
      fetchBodies(popover);
    });

    popover.addEventListener("toggle", (event) => {
      if (!(event instanceof ToggleEvent)) {
        return;
      }
      const opened = event.newState === "open";
      row.setAttribute("aria-expanded", String(opened));
      if (opened) {
        return;
      }
      // Back to the row, unless the reader has already moved on to something else, such
      // as another row whose press closed this popover.
      const focus = document.activeElement;
      if (
        focus === null ||
        focus === document.body ||
        popover.contains(focus) ||
        (row.contains(focus) && focus !== row)
      ) {
        row.focus();
      }
    });
  }

  /** Wire every row with detail on the page. */
  function init() {
    for (const row of document.querySelectorAll("tr[data-row-popover]")) {
      if (row instanceof HTMLElement) {
        wire(row);
      }
    }
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init, { once: true });
  } else {
    init();
  }
})();
