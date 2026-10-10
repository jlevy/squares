// The reader's colour theme: System, Light or Dark, chosen from the gear at the end of
// the navigation bar and kept across pages and visits.
//
// The choice is kpress's own reader preference, the `kpress.theme` key its head
// bootstrap reads before first paint to stamp `data-kpress-theme` (the mode) and
// `data-kpress-resolved-theme` (light or dark) on the root, so a stored choice is in
// place before anything is drawn and this script adds no parallel mechanism. What it
// adds is the part kpress's standalone page leaves out when its runtime is not loaded:
// changing the choice, following the system theme while it is chosen, and following a
// choice made in another page of the site, which is how a page framed in a card's
// popover (`?view=embed`, no navigation bar) keeps to the theme its parent picked.
//
// A change is announced as `squares:themechange` on the document, for the scripts that
// draw with the theme's colours on a canvas.
(() => {
  const storageKey = "kpress.theme";
  const root = document.documentElement;
  /** @type {readonly string[]} */
  const modes = ["system", "light", "dark"];
  const dark = globalThis.matchMedia?.("(prefers-color-scheme: dark)") ?? null;

  /**
   * @param {string | null | undefined} mode
   * @returns {"system" | "light" | "dark"}
   */
  const normalize = (mode) =>
    mode === "light" || mode === "dark" || mode === "system" ? mode : "system";

  /** @returns {string | null} */
  const stored = () => {
    try {
      return localStorage.getItem(storageKey);
    } catch {
      // Storage can throw in a private or sandboxed context; the page keeps its theme.
      return null;
    }
  };

  /** @param {string} mode */
  const store = (mode) => {
    try {
      localStorage.setItem(storageKey, mode);
    } catch {
      // Unstorable: the choice holds for this page only.
    }
  };

  const items = /** @type {HTMLButtonElement[]} */ ([
    ...document.querySelectorAll(".site-theme-menu [data-theme-choice]"),
  ]).filter((item) => modes.includes(item.dataset.themeChoice ?? ""));

  /**
   * Stamp the mode and its resolution on the root, as kpress's bootstrap does, and mark
   * the menu's current choice.
   *
   * @param {string | null | undefined} requested
   */
  const apply = (requested) => {
    const mode = normalize(requested);
    const resolved = mode === "system" ? (dark?.matches ? "dark" : "light") : mode;
    const changed =
      root.dataset.kpressTheme !== mode || root.dataset.kpressResolvedTheme !== resolved;
    root.dataset.kpressTheme = mode;
    root.dataset.kpressResolvedTheme = resolved;
    for (const item of items) {
      item.setAttribute("aria-checked", item.dataset.themeChoice === mode ? "true" : "false");
    }
    if (changed) {
      document.dispatchEvent(
        new CustomEvent("squares:themechange", { detail: { mode, resolved } }),
      );
    }
  };

  apply(stored() ?? root.dataset.kpressTheme);
  dark?.addEventListener("change", () => {
    if (root.dataset.kpressTheme === "system") {
      apply("system");
    }
  });
  // Another page of the site changed the choice: this tab's other pages, or the parent of
  // a framed page. `storage` fires in every same-origin document but the one that wrote.
  window.addEventListener("storage", (event) => {
    if (event.key === storageKey || event.key === null) {
      apply(stored());
    }
  });

  const button = document.querySelector(".site-theme-button");
  const menu = document.getElementById("site-theme-menu");
  if (!(button instanceof HTMLButtonElement) || !(menu instanceof HTMLElement) || !menu.popover) {
    return;
  }

  /** Put the menu under the gear, its right edge on the gear's, inside the window. */
  const place = () => {
    const anchor = button.getBoundingClientRect();
    const width = menu.offsetWidth;
    const left = Math.max(8, Math.min(anchor.right - width, window.innerWidth - width - 8));
    menu.style.left = `${left}px`;
    menu.style.right = "auto";
    menu.style.top = `${anchor.bottom + 4}px`;
  };

  /** @param {number} index */
  const focusItem = (index) => {
    const item = items[(index + items.length) % items.length];
    item?.focus();
  };

  // `beforetoggle` fires as the state changes, `toggle` only after, and the menu has a
  // size to place by only once it is open.
  menu.addEventListener("beforetoggle", (event) => {
    const opening = event instanceof ToggleEvent && event.newState === "open";
    button.setAttribute("aria-expanded", opening ? "true" : "false");
  });
  menu.addEventListener("toggle", (event) => {
    if (event instanceof ToggleEvent && event.newState === "open") {
      place();
      const current = items.findIndex((item) => item.getAttribute("aria-checked") === "true");
      focusItem(Math.max(current, 0));
    }
  });

  for (const item of items) {
    item.addEventListener("click", () => {
      const mode = normalize(item.dataset.themeChoice);
      store(mode);
      apply(mode);
      menu.hidePopover();
      button.focus();
    });
  }

  menu.addEventListener("keydown", (event) => {
    const at = items.indexOf(/** @type {HTMLButtonElement} */ (document.activeElement));
    const moves = /** @type {Record<string, number>} */ ({
      ArrowDown: at + 1,
      ArrowUp: at - 1,
      End: items.length - 1,
      Home: 0,
    });
    if (event.key in moves) {
      event.preventDefault();
      focusItem(moves[event.key] ?? 0);
    } else if (event.key === "Tab") {
      menu.hidePopover();
    } else if (event.key === "Escape") {
      // The popover closes itself on Escape; focus goes back to the gear that opened it.
      button.focus();
    }
  });

  // The bar scrolls sideways on a phone, and the window resizes: keep the menu on its gear.
  window.addEventListener("resize", () => {
    if (menu.matches(":popover-open")) {
      place();
    }
  });
  window.addEventListener(
    "scroll",
    () => {
      if (menu.matches(":popover-open")) {
        place();
      }
    },
    { passive: true },
  );
  document.addEventListener("squares:headerchange", () => {
    if (menu.matches(":popover-open")) {
      place();
    }
  });
  button.closest(".site-nav-inner")?.addEventListener("scroll", () => {
    if (menu.matches(":popover-open")) {
      place();
    }
  });
})();
