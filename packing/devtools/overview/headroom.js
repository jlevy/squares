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
  const initialTop = header.getBoundingClientRect().top + window.scrollY;
  // A little tolerance ignores touch jitter, while a small reversal exposes navigation
  // without asking a reader to travel back through a full header's height.
  const revealDistance = 2;
  const hideDistance = 6;
  const anchorGap = 8;
  let height = 0;
  let topRegion = 0;
  let pending = false;
  let lastScroll = Math.max(0, window.scrollY);
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
    lastScroll = scrollPosition();
    directionStart = lastScroll;
    direction = 0;
    setHidden(false);
  };

  const measure = () => {
    const measured = header.getBoundingClientRect().height;
    if (height !== measured) {
      height = measured;
      topRegion = initialTop + height;
      root.style.setProperty("--site-header-offset", `${height + anchorGap}px`);
      // A face loading or a wrapped row changes the geometry, not scroll intent.
      // Keep a hidden header hidden while updating its full anchor clearance.
      schedule();
      document.dispatchEvent(new CustomEvent("squares:headerchange"));
    }
  };

  const update = () => {
    pending = false;
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

  header.classList.add("site-headroom");
  measure();
  window.addEventListener("scroll", schedule, { passive: true });
  window.addEventListener("resize", () => {
    measure();
    reset();
  });
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
