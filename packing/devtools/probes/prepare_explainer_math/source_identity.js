// Which page was measured: its title, publication date and source revision link.
() => ({
  title: document.title,
  publication_date: document.querySelector(".publication-date")?.textContent || null,
  revision_url:
    /** @type {HTMLAnchorElement | null} */ (
      document.querySelector('a[href*="github.com/jlevy/squares/blob/"]')
    )?.href || null,
});
