// A compact disclosure around ordinary multi-select filter buttons. The caller owns
// selection and URL state; this component owns focus, dismissal and the summary.
(() => {
  for (const root of document.querySelectorAll("[data-site-filter-menu]")) {
    if (!(root instanceof HTMLElement) || root.dataset.siteFilterReady) {
      continue;
    }
    const trigger = root.querySelector("[data-site-filter-trigger]");
    const panel = root.querySelector("[data-site-filter-options]");
    const summary = root.querySelector("[data-site-filter-summary]");
    if (
      !(trigger instanceof HTMLButtonElement) ||
      !(panel instanceof HTMLElement) ||
      !(summary instanceof HTMLElement)
    ) {
      continue;
    }
    const options = [...panel.querySelectorAll("button[data-site-filter-option]")].filter(
      (option) => option instanceof HTMLButtonElement,
    );
    const all = panel.querySelector("[data-site-filter-all]");
    const items = [...panel.querySelectorAll("button")].filter(
      (option) => option instanceof HTMLButtonElement && !option.disabled,
    );
    const refresh = () => {
      const chosen = options.filter((option) => option.getAttribute("aria-pressed") === "true");
      const complete = chosen.length === options.length;
      all?.setAttribute("aria-pressed", String(complete));
      summary.replaceChildren();
      if (complete || chosen.length === 0) {
        summary.textContent = complete ? "All" : "None";
      } else {
        const first = chosen[0];
        const chip = first?.querySelector("[data-site-filter-label]")?.cloneNode(true);
        if (chip instanceof HTMLElement && first) {
          // Clone only the semantic chip label, never its tally, check or interaction.
          chip.classList.add("site-chip");
          for (const [key, value] of Object.entries(first.dataset)) {
            if (!key.startsWith("siteFilter")) {
              chip.dataset[key] = value;
            }
          }
          summary.append(chip);
        }
        if (chosen.length > 1) {
          summary.append(document.createTextNode(` +${chosen.length - 1}`));
        }
      }
    };
    const fit = () => {
      panel.style.translate = "0px";
      const bounds = panel.getBoundingClientRect();
      const shift = Math.max(16 - bounds.left, Math.min(0, innerWidth - 16 - bounds.right));
      panel.style.translate = `${shift}px`;
    };
    /** @param {boolean} open @param {boolean} [restoreFocus] */
    const setOpen = (open, restoreFocus = false) => {
      if (!open && (restoreFocus || panel.contains(document.activeElement))) {
        trigger.focus();
      }
      trigger.setAttribute("aria-expanded", String(open));
      panel.hidden = !open;
      panel.inert = !open;
      if (open) {
        fit();
      }
    };
    trigger.addEventListener("click", () => {
      setOpen(trigger.getAttribute("aria-expanded") !== "true");
    });
    root.addEventListener("keydown", (event) => {
      if (event.key === "Escape" && trigger.getAttribute("aria-expanded") === "true") {
        event.preventDefault();
        event.stopPropagation();
        setOpen(false, true);
        return;
      }
      if (!["ArrowDown", "ArrowUp", "Home", "End"].includes(event.key)) {
        return;
      }
      event.preventDefault();
      setOpen(true);
      const active = document.activeElement;
      const at = active instanceof HTMLButtonElement ? items.indexOf(active) : -1;
      const last = items.length - 1;
      const next =
        event.key === "Home"
          ? 0
          : event.key === "End"
            ? last
            : event.key === "ArrowDown"
              ? (at + 1) % items.length
              : at < 0
                ? last
                : (at - 1 + items.length) % items.length;
      items[next]?.focus();
    });
    root.addEventListener("focusout", (event) => {
      if (!(event.relatedTarget instanceof Node) || !root.contains(event.relatedTarget)) {
        setOpen(false);
      }
    });
    document.addEventListener("pointerdown", (event) => {
      if (!(event.target instanceof Node) || !root.contains(event.target)) {
        setOpen(false);
      }
    });
    document.addEventListener("squares:filterschange", refresh);
    window.addEventListener("resize", () => {
      if (!panel.hidden) {
        fit();
      }
    });
    setOpen(false);
    refresh();
    root.dataset.siteFilterReady = "true";
  }
})();
