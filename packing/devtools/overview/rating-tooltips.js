// Rating and case-property explanations use KPress's tooltip placement and surface.
(() => {
  const position = globalThis.siteKpressTooltipPosition;
  if (!position) {
    return;
  }
  const place = position;
  const selector =
    ".site-atlas-badge[title], .site-significance[title], button[data-news-score][title], .site-chip.site-rung-fill[title], .site-star[title], .badge-item[title]";
  /** @type {{ trigger: HTMLElement; tooltip: HTMLElement } | null} */
  let active = null;
  let pendingShow = 0;
  let pendingHide = 0;
  let sequence = 0;

  function clearTimers() {
    window.clearTimeout(pendingShow);
    window.clearTimeout(pendingHide);
  }

  function hide() {
    clearTimers();
    const previous = active;
    active = null;
    if (!previous) {
      return;
    }
    const { trigger, tooltip } = previous;
    const remaining = (trigger.getAttribute("aria-describedby") || "")
      .split(/\s+/)
      .filter((id) => id && id !== tooltip.id);
    if (remaining.length) {
      trigger.setAttribute("aria-describedby", remaining.join(" "));
    } else {
      trigger.removeAttribute("aria-describedby");
    }
    tooltip.setAttribute("aria-hidden", "true");
    tooltip.classList.remove("kpress-tooltip-visible");
    const duration = Number.parseFloat(getComputedStyle(tooltip).transitionDuration) * 1000;
    if (!duration) {
      tooltip.remove();
      return;
    }
    tooltip.addEventListener("transitionend", () => tooltip.remove(), { once: true });
    window.setTimeout(() => tooltip.remove(), duration + 100);
  }

  /** @param {HTMLElement} trigger */
  function show(trigger) {
    clearTimers();
    if (active?.trigger === trigger || !trigger.isConnected) {
      return;
    }
    hide();
    const tooltip = document.createElement("aside");
    tooltip.className = "kpress-tooltip site-rating-tooltip kpress-no-print";
    tooltip.setAttribute("role", "tooltip");
    tooltip.setAttribute("popover", "manual");
    do {
      tooltip.id = `site-rating-tooltip-${++sequence}`;
    } while (document.getElementById(tooltip.id));
    tooltip.textContent = trigger.dataset.siteTooltip || "";
    // KPress mounts the overlay in its viewport. Open it in the top layer before
    // the second placement pass measures it, so a case/result popover cannot clip it.
    place(/** @type {HTMLAnchorElement} */ (trigger), tooltip);
    tooltip.showPopover();
    fit(trigger, tooltip);
    trigger.setAttribute(
      "aria-describedby",
      [trigger.getAttribute("aria-describedby"), tooltip.id].filter(Boolean).join(" "),
    );
    active = { trigger, tooltip };
    tooltip.addEventListener("pointerenter", clearTimers);
    tooltip.addEventListener("pointerleave", delayHide);
    requestAnimationFrame(() => {
      requestAnimationFrame(() => {
        if (active?.tooltip === tooltip) {
          tooltip.classList.add("kpress-tooltip-visible");
        }
      });
    });
  }

  /** @param {HTMLElement} tooltip @param {number} dx @param {number} dy */
  function shift(tooltip, dx, dy) {
    const style = getComputedStyle(tooltip);
    const left = Number.parseFloat(style.left);
    const top = Number.parseFloat(style.top);
    if (dx) {
      tooltip.style.insetInlineStart = "";
      tooltip.style.insetInlineEnd = "";
      tooltip.style.left = `${left + dx}px`;
    }
    if (dy) {
      tooltip.style.top = `${top + dy}px`;
    }
  }

  /** Where the site header ends while it is shown, or 0 while headroom hides it. The
   * explanation lies in the top layer, over the header, so its links count as controls
   * too. A header still sliding into view counts at its resting place. */
  function headerBottom() {
    const header =
      document.querySelector(".site-headroom") ?? document.querySelector(".kpress-site-header");
    if (
      !(header instanceof HTMLElement) ||
      (header.matches(".site-headroom-hidden") &&
        !header.matches(":focus-within, :has(.site-theme-menu:popover-open)"))
    ) {
      return 0;
    }
    const transform = getComputedStyle(header).transform;
    const travel = transform && transform !== "none" ? new DOMMatrixReadOnly(transform).m42 : 0;
    return Math.max(0, header.getBoundingClientRect().bottom - travel);
  }

  /** @param {HTMLElement} trigger @param {HTMLElement} tooltip */
  function fit(trigger, tooltip) {
    place(/** @type {HTMLAnchorElement} */ (trigger), tooltip);
    // KPress prefers below-table callouts. Fit their measured box when a row is
    // near a viewport edge, preserving its normal placement and mobile bottom bar.
    if (!tooltip.classList.contains("kpress-tooltip-mobile-bottom")) {
      // A trigger among controls, the News filters, explains itself above them, below
      // the shown site header, or below them where there is no room between: an
      // explanation is hoverable, so one lying over a control would take its click.
      const block = trigger.closest("[data-site-tooltip-outside]");
      if (block) {
        const around = block.getBoundingClientRect();
        const rect = tooltip.getBoundingClientRect();
        const above = around.top - 8 - rect.height;
        shift(
          tooltip,
          trigger.getBoundingClientRect().left - rect.left,
          (above >= Math.max(10, headerBottom() + 8) ? above : around.bottom + 8) - rect.top,
        );
      }
      const rect = tooltip.getBoundingClientRect();
      shift(
        tooltip,
        Math.max(
          10 - rect.left,
          Math.min(0, document.documentElement.clientWidth - 10 - rect.right),
        ),
        Math.max(10 - rect.top, Math.min(0, window.innerHeight - 10 - rect.bottom)),
      );
    }
  }

  function delayHide() {
    window.clearTimeout(pendingShow);
    window.clearTimeout(pendingHide);
    pendingHide = window.setTimeout(() => {
      if (
        active &&
        document.activeElement !== active.trigger &&
        !active.trigger.matches(":hover") &&
        !active.tooltip.matches(":hover")
      ) {
        hide();
      }
    }, 200);
  }

  /** @param {HTMLElement} trigger */
  function prepare(trigger) {
    const meaning = trigger.getAttribute("title")?.trim();
    if (!meaning) {
      return;
    }
    const rung =
      trigger.classList.contains("site-significance") || trigger.dataset.newsScore
        ? `S${trigger.dataset.level || trigger.dataset.newsScore}`
        : trigger.classList.contains("site-rung-fill")
          ? trigger.textContent?.trim() || ""
          : "";
    const scale = { S: "Significance", V: "Verification", C: "Confirmation" }[
      /** @type {"S" | "V" | "C"} */ (rung.charAt(0))
    ];
    trigger.dataset.siteTooltip = rung ? `${scale} ${rung}: ${meaning}` : meaning;
    // Source titles remain a useful no-JS fallback. Enhanced badges have one tooltip.
    trigger.removeAttribute("title");
    trigger.removeAttribute("aria-hidden");
    if (!(trigger instanceof HTMLButtonElement)) {
      trigger.setAttribute("role", "img");
    }
    if (!trigger.hasAttribute("aria-label")) {
      trigger.setAttribute("aria-label", rung ? `${scale} ${rung}` : meaning);
    }
    if (!trigger.hasAttribute("tabindex")) {
      trigger.tabIndex = 0;
    }
    trigger.addEventListener("pointerenter", () => {
      clearTimers();
      pendingShow = window.setTimeout(() => show(trigger), 500);
    });
    trigger.addEventListener("pointerleave", delayHide);
    // A native button takes focus on a mouse press too; only keyboard focus explains it,
    // so a click never flashes the explanation it then dismisses.
    trigger.addEventListener("focus", () => {
      if (!(trigger instanceof HTMLButtonElement) || trigger.matches(":focus-visible")) {
        show(trigger);
      }
    });
    trigger.addEventListener("blur", delayHide);
    // A native button's press is its own action, a News filter's toggle: its explanation
    // steps aside, so it never covers the controls a reader goes to next. Hover and
    // keyboard focus still show it. Any other trigger shows its explanation on a press.
    trigger.addEventListener("click", (event) => {
      if (trigger instanceof HTMLButtonElement) {
        hide();
        return;
      }
      event.preventDefault();
      event.stopPropagation();
      show(trigger);
    });
    trigger.addEventListener("keydown", (event) => {
      if (event.key === "Enter" || event.key === " ") {
        if (trigger instanceof HTMLButtonElement) {
          hide();
          return;
        }
        event.preventDefault();
        event.stopPropagation();
        show(trigger);
      }
    });
  }

  /** @param {ParentNode} root */
  function scan(root) {
    if (root instanceof HTMLElement && root.matches(selector)) {
      prepare(root);
    }
    for (const trigger of root.querySelectorAll(selector)) {
      if (trigger instanceof HTMLElement) {
        prepare(trigger);
      }
    }
  }

  function boot() {
    scan(document);
    new MutationObserver((records) => {
      for (const record of records) {
        for (const node of record.addedNodes) {
          if (node instanceof HTMLElement) {
            scan(node);
          }
        }
      }
      if (active && (!active.trigger.isConnected || !active.tooltip.isConnected)) {
        hide();
      }
    }).observe(document.body, { childList: true, subtree: true });
    document.addEventListener(
      "keydown",
      (event) => {
        if (event.key === "Escape" && active) {
          event.preventDefault();
          event.stopImmediatePropagation();
          hide();
        }
      },
      true,
    );
    document.addEventListener("pointerdown", (event) => {
      if (
        active &&
        event.target instanceof Node &&
        !active.trigger.contains(event.target) &&
        !active.tooltip.contains(event.target)
      ) {
        hide();
      }
    });
    document.addEventListener(
      "toggle",
      (event) => {
        if (
          event.target instanceof HTMLElement &&
          event.target.matches(".site-popover") &&
          !event.target.matches(":popover-open")
        ) {
          hide();
        }
      },
      true,
    );
    window.addEventListener("resize", hide);
    // A header that headroom shows or hides moves the room above a block of controls.
    document.addEventListener("squares:headerchange", () => {
      if (active) {
        fit(active.trigger, active.tooltip);
      }
    });
    document.addEventListener(
      "scroll",
      () => {
        // Focus may scroll the badge into view after its focus event. Keep its
        // explanation attached; pointer-only explanations dismiss while scrolling.
        if (active && document.activeElement === active.trigger) {
          fit(active.trigger, active.tooltip);
        } else {
          hide();
        }
      },
      true,
    );
  }
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", boot, { once: true });
  } else {
    boot();
  }
})();
