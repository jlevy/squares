// News entry cards keep their actual articles; presses only change the visible height.
// Without this enhancement, the complete articles and their ordinary links stay visible.
(() => {
  /** @type {Map<Element, (open: boolean) => void>} */
  const cards = new Map();
  /** @type {Map<Element, () => void>} */
  const refreshers = new Map();
  for (const card of document.querySelectorAll("[data-news-day]")) {
    const button = card.querySelector(".site-news-expand");
    const body = card.querySelector(".site-news-body");
    if (
      !(card instanceof HTMLElement) ||
      !(button instanceof HTMLButtonElement) ||
      !(body instanceof HTMLElement)
    ) {
      continue;
    }
    const date = card.querySelector("time")?.textContent ?? card.dataset.newsDay;
    const setOpen = (/** @type {boolean} */ open, animate = true) => {
      if (card.dataset.newsEnhanced && (button.getAttribute("aria-expanded") === "true") === open) {
        return;
      }
      if (animate) {
        body.style.maxBlockSize = `${body.getBoundingClientRect().height}px`;
        // Commit the current height so rapid presses reverse from the visible frame.
        body.getBoundingClientRect();
      }
      card.classList.toggle("is-collapsed", !open);
      body.style.maxBlockSize = open ? `${body.scrollHeight}px` : "10lh";
      if (open && window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
        body.style.removeProperty("max-block-size");
      }
      button.setAttribute("aria-expanded", String(open));
      button.setAttribute("aria-label", `${open ? "Collapse" : "Expand"} news for ${date}`);
      const arrow = button.querySelector("[data-arrow]");
      arrow?.setAttribute("data-arrow", open ? "double-up" : "double-down");
    };
    body.addEventListener("transitionend", (event) => {
      if (
        event.target === body &&
        ["max-block-size", "max-height"].includes(event.propertyName) &&
        button.getAttribute("aria-expanded") === "true"
      ) {
        body.style.removeProperty("max-block-size");
      }
    });
    const refresh = () => {
      if (!card.getClientRects().length) {
        return;
      }
      const wasShort = button.hidden;
      if (!card.dataset.newsEnhanced) {
        setOpen(false, false);
      }
      const limit = 10 * Number.parseFloat(getComputedStyle(body).lineHeight);
      const short = body.scrollHeight <= limit + 1;
      button.hidden = short;
      if (short) {
        setOpen(true, false);
        body.style.removeProperty("max-block-size");
      } else if (wasShort) {
        setOpen(false, false);
      } else if (button.getAttribute("aria-expanded") === "true") {
        body.style.removeProperty("max-block-size");
      }
      card.dataset.newsEnhanced = "true";
    };
    const toggle = () => {
      if (!button.hidden) {
        setOpen(button.getAttribute("aria-expanded") !== "true");
      }
    };
    button.addEventListener("click", toggle);
    body.addEventListener("focusin", (event) => {
      if (event.target instanceof Element && event.target.closest("[data-site-tooltip]")) {
        return;
      }
      setOpen(true);
    });
    card.addEventListener("click", (event) => {
      if (
        !(event.target instanceof Element) ||
        event.target.closest(
          "a, button, input, select, textarea, summary, details, [contenteditable]",
        ) ||
        window.getSelection()?.isCollapsed === false
      ) {
        return;
      }
      toggle();
    });
    cards.set(card, setOpen);
    refreshers.set(card, refresh);
    refresh();
    let previousWidth = card.getBoundingClientRect().width;
    new ResizeObserver(() => {
      const width = card.getBoundingClientRect().width;
      if (width > 0 && Math.abs(width - previousWidth) > 0.5) {
        previousWidth = width;
        refresh();
      }
    }).observe(card);
  }
  const reveal = () => {
    let id;
    try {
      id = decodeURIComponent(location.hash.slice(1));
    } catch {
      return;
    }
    const card = document.getElementById(id)?.closest("[data-news-day]");
    if (card) {
      cards.get(card)?.(true);
    }
  };
  reveal();
  document.addEventListener("news:filter", () => {
    for (const refresh of refreshers.values()) {
      refresh();
    }
    reveal();
  });
  window.addEventListener("hashchange", reveal);
})();
