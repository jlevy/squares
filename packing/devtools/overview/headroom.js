// Every shell keeps its whole header in the document flow. Sticky positioning makes it
// reachable on the first upward movement; only its paint moves, never the page below it.
(() => {
  const root = document.documentElement;
  const nav = document.querySelector(".site-nav");
  if (!(nav instanceof HTMLElement) || root.dataset.siteView === "embed") {
    return;
  }
  const header = nav.closest(".site-app-shell") ?? nav.closest(".kpress-site-header") ?? nav;
  if (!(header instanceof HTMLElement)) {
    return;
  }

  const menu = header.querySelector(".site-theme-menu");
  // A little tolerance ignores touch jitter, while a small reversal exposes navigation
  // without asking a reader to travel back through a full header's height.
  const revealDistance = 2;
  const hideDistance = 6;
  const anchorGap = 8;
  let initialTop = 0;
  let measuredLayout = false;
  let height = 0;
  let topRegion = 0;
  let pending = false;
  let lastScroll = 0;
  let directionStart = lastScroll;
  let direction = 0;
  let hidden = false;

  /** @param {boolean} nextHidden */
  const setHidden = (nextHidden) => {
    if (hidden !== nextHidden) {
      hidden = nextHidden;
      header.classList.toggle("site-headroom-hidden", hidden);
      document.dispatchEvent(new CustomEvent("squares:headerchange"));
    }
  };

  const scrollPosition = () => {
    const maximum = Math.max(0, root.scrollHeight - window.innerHeight);
    // Safari can report positions beyond either document edge during touch overscroll.
    return Math.max(0, Math.min(window.scrollY, maximum));
  };

  const reset = () => {
    lastScroll = measuredLayout ? scrollPosition() : 0;
    directionStart = lastScroll;
    direction = 0;
    setHidden(false);
  };

  /** @param {ResizeObserverEntry[]} entries */
  const measure = (entries) => {
    const entry = entries[0];
    if (!entry) {
      return;
    }
    // ResizeObserver delivers geometry after layout. Reading it here avoids charging
    // the complete page's first layout to the navigation's startup script.
    const measured = entry.borderBoxSize[0]?.blockSize ?? header.getBoundingClientRect().height;
    /** @type {number | undefined} */
    let initialAnchorScroll;
    if (!measuredLayout) {
      // Capture the normal-flow origin before sticky positioning, including a first
      // delivery after fragment navigation or restored history has scrolled the page.
      initialTop = header.getBoundingClientRect().top + window.scrollY;
      lastScroll = Math.max(0, window.scrollY);
      if (lastScroll > 0 && location.hash) {
        let fragment = location.hash.slice(1);
        try {
          fragment = decodeURIComponent(fragment);
        } catch {
          // A malformed escaped fragment can still name a literal document ID.
        }
        const target = document.getElementById(fragment);
        if (target && target.getClientRects().length > 0) {
          const targetTop = target.getBoundingClientRect().top;
          // Preserve a native fragment arrival's clearance; a restored reader position
          // far above or below that target is independent and must remain untouched.
          if (targetTop >= -0.5 && targetTop < measured + anchorGap) {
            initialAnchorScroll = Math.max(0, lastScroll + targetTop - measured - anchorGap);
            lastScroll = initialAnchorScroll;
          }
        }
      }
      directionStart = lastScroll;
      measuredLayout = true;
      header.classList.add("site-headroom");
    }
    if (height !== measured) {
      height = measured;
      topRegion = initialTop + height;
      root.style.setProperty("--site-header-offset", `${height + anchorGap}px`);
      // A face loading or a wrapped row changes the geometry, not scroll intent.
      // Keep a hidden header hidden while updating its full anchor clearance.
      document.dispatchEvent(new CustomEvent("squares:headerchange"));
    }
    if (initialAnchorScroll !== undefined) {
      window.scrollTo({ top: initialAnchorScroll, behavior: "instant" });
    }
  };

  const update = () => {
    pending = false;
    if (!measuredLayout) {
      return;
    }
    const position = scrollPosition();
    const delta = position - lastScroll;
    const nextDirection = Math.sign(delta);
    if (nextDirection !== 0 && nextDirection !== direction) {
      direction = nextDirection;
      directionStart = lastScroll;
    }
    const protectedHeader =
      header.contains(document.activeElement) ||
      (menu instanceof HTMLElement && menu.matches(":popover-open"));
    if (position <= topRegion || protectedHeader) {
      setHidden(false);
    } else if (direction < 0 && directionStart - position >= revealDistance) {
      setHidden(false);
    } else if (direction > 0 && position - directionStart >= hideDistance) {
      setHidden(true);
    }
    lastScroll = position;
  };

  const schedule = () => {
    if (!pending) {
      pending = true;
      requestAnimationFrame(update);
    }
  };

  window.addEventListener("scroll", schedule, { passive: true });
  window.addEventListener("resize", reset);
  // In-page navigation and restored history positions start with reachable navigation.
  window.addEventListener("hashchange", reset);
  window.addEventListener("popstate", reset);
  window.addEventListener("pageshow", (event) => {
    if (event.persisted) {
      reset();
    }
  });
  header.addEventListener("focusin", () => setHidden(false));
  menu?.addEventListener("beforetoggle", (event) => {
    if (event instanceof ToggleEvent && event.newState === "open") {
      setHidden(false);
    }
  });
  new ResizeObserver(measure).observe(header);
})();
