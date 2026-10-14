// Retained About history bookmarks land on the corresponding News item or day.
// The page keeps a visible News link for readers without scripting.
(() => {
  const forward = () => {
    const target = document.getElementById(location.hash.slice(1));
    if (target instanceof HTMLAnchorElement && target.hasAttribute("data-news-target")) {
      location.replace(target.href);
    }
  };
  forward();
  window.addEventListener("hashchange", forward);
})();
