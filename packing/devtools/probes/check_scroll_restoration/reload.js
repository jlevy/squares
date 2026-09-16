// The browser's document navigation API, rather than Playwright's reload command, which in
// WebKit resets even an unmodified document's scroll position.
() => location.reload();
