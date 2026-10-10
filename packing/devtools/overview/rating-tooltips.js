// Rating and case-property explanations use KPress's tooltip placement and surface.
(() => {
  const position = globalThis.siteKpressTooltipPosition;
  if (!position) {
    return;
  }
  const place = position;
  const selector =
    ".site-atlas-badge[title], .site-significance[title], .site-chip.site-rung-fill[title], .site-star[title], .badge-item[title]";
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

  /** @param {HTMLElement} trigger @param {HTMLElement} tooltip */
  function fit(trigger, tooltip) {
    place(/** @type {HTMLAnchorElement} */ (trigger), tooltip);
    // KPress prefers below-table callouts. Fit their measured box when a row is
    // near a viewport edge, preserving its normal placement and mobile bottom bar.
    if (!tooltip.classList.contains("kpress-tooltip-mobile-bottom")) {
      const rect = tooltip.getBoundingClientRect();
      const style = getComputedStyle(tooltip);
      const left = Number.parseFloat(style.left);
      const top = Number.parseFloat(style.top);
      const dx = Math.max(
        10 - rect.left,
        Math.min(0, document.documentElement.clientWidth - 10 - rect.right),
      );
      const dy = Math.max(10 - rect.top, Math.min(0, window.innerHeight - 10 - rect.bottom));
      if (dx) {
        tooltip.style.insetInlineStart = "";
        tooltip.style.insetInlineEnd = "";
        tooltip.style.left = `${left + dx}px`;
      }
      if (dy) {
        tooltip.style.top = `${top + dy}px`;
      }
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
    const rung = trigger.classList.contains("site-significance")
      ? `S${trigger.dataset.level}`
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
    trigger.setAttribute("role", "img");
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
    trigger.addEventListener("focus", () => show(trigger));
    trigger.addEventListener("blur", delayHide);
    trigger.addEventListener("click", (event) => {
      event.preventDefault();
      event.stopPropagation();
      show(trigger);
    });
    trigger.addEventListener("keydown", (event) => {
      if (event.key === "Enter" || event.key === " ") {
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
