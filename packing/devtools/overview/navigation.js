// Ordinary site links keep their browser behavior. Buttons only disclose their lists.
(() => {
  const nav = document.querySelector(".site-nav");
  if (!(nav instanceof HTMLElement)) {
    return;
  }
  const mobile = nav.querySelector(".site-nav-mobile-toggle");
  if (!(mobile instanceof HTMLButtonElement)) {
    return;
  }
  const narrow = window.matchMedia("(width < 48rem)");
  const disclosures = Array.from(nav.querySelectorAll(".site-nav-disclosure")).filter(
    (button) => button instanceof HTMLButtonElement,
  );

  /** @param {HTMLButtonElement} button */
  const panelFor = (button) => document.getElementById(button.getAttribute("aria-controls") ?? "");

  /** @param {HTMLButtonElement} button @param {boolean} open @param {boolean} [restoreFocus] */
  const setOpen = (button, open, restoreFocus = false) => {
    const panel = panelFor(button);
    if (!(panel instanceof HTMLElement)) {
      return;
    }
    if (!open && (restoreFocus || panel.contains(document.activeElement))) {
      button.focus();
    }
    button.setAttribute("aria-expanded", String(open));
    panel.hidden = !open;
    nav.classList.toggle(
      "site-nav-disclosed",
      disclosures.some((control) => control.getAttribute("aria-expanded") === "true"),
    );
    nav.dispatchEvent(new CustomEvent("squares:navigationchange", { bubbles: true }));
  };

  const closeDisclosures = () => {
    for (const button of disclosures) {
      if (button.getAttribute("aria-expanded") === "true") {
        setOpen(button, false);
      }
    }
  };

  /** @param {boolean} open @param {boolean} [restoreFocus] */
  const setMobileOpen = (open, restoreFocus = false) => {
    if (!open) {
      closeDisclosures();
      const list = panelFor(mobile);
      if (restoreFocus || list?.contains(document.activeElement)) {
        mobile.focus();
      }
    }
    mobile.setAttribute("aria-expanded", String(open));
    nav.classList.toggle("site-nav-mobile-open", open);
    nav.dispatchEvent(new CustomEvent("squares:navigationchange", { bubbles: true }));
  };

  for (const button of disclosures) {
    const panel = panelFor(button);
    if (!(panel instanceof HTMLElement)) {
      continue;
    }
    panel.hidden = true;
    button.addEventListener("click", () => {
      const open = button.getAttribute("aria-expanded") !== "true";
      closeDisclosures();
      if (open) {
        for (const popover of document.querySelectorAll("[popover]:popover-open")) {
          if (popover instanceof HTMLElement) {
            popover.hidePopover();
          }
        }
      }
      setOpen(button, open);
    });
    button.addEventListener("keydown", (event) => {
      if (event.key !== "ArrowDown" && event.key !== "ArrowUp") {
        return;
      }
      event.preventDefault();
      closeDisclosures();
      setOpen(button, true);
      const links = panel.querySelectorAll("a");
      const link = event.key === "ArrowDown" ? links[0] : links[links.length - 1];
      link?.focus();
    });
  }
  nav.dataset.siteNavReady = "true";
  mobile.addEventListener("click", () =>
    setMobileOpen(mobile.getAttribute("aria-expanded") !== "true"),
  );
  nav.addEventListener("keydown", (event) => {
    if (event.key !== "Escape") {
      return;
    }
    const open = disclosures.find((button) => button.getAttribute("aria-expanded") === "true");
    if (open) {
      event.preventDefault();
      event.stopPropagation();
      setOpen(open, false, true);
    } else if (mobile.getAttribute("aria-expanded") === "true") {
      event.preventDefault();
      event.stopPropagation();
      setMobileOpen(false, true);
    }
  });
  document.addEventListener("click", (event) => {
    if (!(event.target instanceof Node)) {
      return;
    }
    if (!nav.contains(event.target)) {
      closeDisclosures();
      setMobileOpen(false);
    } else if (event.target instanceof Element && event.target.closest("a")) {
      closeDisclosures();
      setMobileOpen(false);
    }
  });
  document.addEventListener("focusin", (event) => {
    if (event.target instanceof Node && !nav.contains(event.target)) {
      closeDisclosures();
      setMobileOpen(false);
    }
  });
  // Theme and article popovers own the top layer; their opening dismisses the links.
  document.addEventListener(
    "beforetoggle",
    (event) => {
      if (event instanceof ToggleEvent && event.newState === "open") {
        closeDisclosures();
        setMobileOpen(false);
      }
    },
    true,
  );
  narrow.addEventListener("change", () => {
    closeDisclosures();
    setMobileOpen(false);
  });
})();
