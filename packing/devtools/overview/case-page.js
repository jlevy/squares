// Registered forwarding: known legacy case-index aliases resolve to complete records.
// The static index links are the authority for known counts; ordinary links navigate
// to complete pages. A valid ?n takes precedence over #n-N. Meaningful record fragments
// and embedding state survive; invalid counts leave the reader at the index.
(() => {
  const url = new URL(location.href);
  const query = url.searchParams.get("n");
  const fragment = /^#n-(\d+)$/.exec(url.hash)?.[1];
  const digits = query !== null && /^\d+$/.test(query) ? query : fragment;
  if (digits === undefined) {
    return;
  }
  const n = String(Number(digits));
  const link = document.querySelector(`nav[data-case-index] a[data-case="${n}"]`);
  if (!(link instanceof HTMLAnchorElement)) {
    return;
  }
  const target = new URL(link.href, location.href);
  url.searchParams.delete("n");
  target.search = url.search;
  target.hash = fragment === undefined ? url.hash : "";
  location.replace(target.href);
})();
