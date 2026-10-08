// Input response: table rows open a detail overlay. Ordinary result links also open
// the complete canonical page without JavaScript. On the first opening, the overlay
// fetches that page, extracts its prepared article and resolves relative links against
// the response URL. Sorting and filtering preserve each row's named overlay.
(() => {
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
      void fetch(source)
        .then(async (response) => {
          if (!response.ok) {
            throw new Error(String(response.status));
          }
          const held = document.createElement("template");
          held.innerHTML = await response.text();
          const article = held.content.querySelector("article.site-result[data-result-overview]");
          if (!(article instanceof HTMLElement)) {
            throw new Error("The result page has no record article");
          }
          for (const node of article.querySelectorAll("[href], [src]")) {
            for (const attribute of ["href", "src"]) {
              const value = node.getAttribute(attribute);
              if (value === null || value.startsWith("#")) {
                continue;
              }
              node.setAttribute(
                attribute,
                new URL(value, response.url || new URL(source, document.baseURI).href).href,
              );
            }
          }
          body.replaceChildren(article);
          body.removeAttribute("data-row-pop-src");
        })
        // The short body is already there; a later opening tries again.
        .catch(() => undefined)
        .finally(() => {
          body.removeAttribute("data-row-pop-loading");
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
      popover.showPopover();
      // The toggle event below says the same a task later; the row's wash should not wait.
      row.setAttribute("aria-expanded", "true");
      const close = popover.querySelector(".site-popover-close");
      if (close instanceof HTMLElement) {
        close.focus();
      }
    };

    // A press starts the fetch a moment before the click that opens the popover.
    row.addEventListener("pointerdown", () => {
      fetchBodies(popover);
    });

    row.addEventListener("click", (event) => {
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
      const control = event.target.closest(CONTROLS);
      const trigger = control?.getAttribute("popovertarget") === popover.id;
      if ((control !== null && row.contains(control) && !trigger) || selecting(row)) {
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
      if (!(event instanceof ToggleEvent) || event.newState !== "open") {
        return;
      }
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
