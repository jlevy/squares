// Retained About and retired News bookmarks reach their current destinations.
// The page keeps a visible News link for readers without scripting.
(() => {
  const forward = () => {
    let id;
    try {
      id = decodeURIComponent(location.hash.slice(1));
    } catch {
      return;
    }
    const target = document.getElementById(id);
    if (target instanceof HTMLAnchorElement && target.hasAttribute("data-news-target")) {
      location.replace(target.href);
    }
  };
  forward();
  window.addEventListener("hashchange", forward);
})();
