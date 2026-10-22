// The overview's card popovers. They open and close natively (`popovertarget`), so the
// page works without this script; it adds three things the platform does not:
//   - opening a panel cancels any pending article request, including a native card
//     that has no asynchronous controller of its own;
//   - a formula inside a popover is typeset when the popover opens, since the math driver
//     leaves hidden math until it is shown;
//   - following a link in a popover closes it, so a reader sent to a row on this page
//     lands on the row rather than behind the panel. The popover listens for the click
//     itself, so a link placed in it later, as a row's deferred body is, closes it too.
//     A link to a place inside the panel scrolls the panel there instead, without
//     navigating: a loaded article's IDs are scoped to this page load
//     (`article-loader.js`), so the address and history are no place for them.
(() => {
  for (const popover of document.querySelectorAll(".site-popover[popover]")) {
    if (!(popover instanceof HTMLElement)) {
      continue;
    }
    popover.addEventListener("beforetoggle", (event) => {
      if (event instanceof ToggleEvent && event.newState === "open") {
        globalThis.siteArticles?.cancelRequests();
      }
    });
    popover.addEventListener("toggle", (event) => {
      if (event instanceof ToggleEvent && event.newState === "open") {
        void globalThis.siteMath?.typeset(popover, true);
      }
    });
    popover.addEventListener("click", (event) => {
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
      const link = event.target.closest("a[href]");
      if (!(link instanceof HTMLAnchorElement)) {
        return;
      }
      const href = link.getAttribute("href");
      const local = href?.startsWith("#") ? document.getElementById(href.slice(1)) : null;
      if (local === null || !popover.contains(local)) {
        popover.hidePopover();
        return;
      }
      event.preventDefault();
      local.scrollIntoView({ block: "nearest" });
    });
  }
})();
