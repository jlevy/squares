// Begin counting DOM mutations inside the page's live regions: any element whose nearest
// aria-live, or implied live role, is not "off". An <output> is role="status" unless it
// says otherwise. Returns the regions found, so a count of zero can be told from nothing
// to watch. Read and stop the count with pack/live-count.
() => {
  /** @typedef {{observer: MutationObserver, counts: Record<string, number>, tally: (records: MutationRecord[]) => void}} LiveWatch */
  const holder = /** @type {Window & {packLiveWatch?: LiveWatch}} */ (window);
  /** @param {Element | null} element */
  const regionOf = (element) => {
    for (let at = element; at !== null; at = at.parentElement) {
      const live = at.getAttribute("aria-live");
      if (live !== null) {
        return live === "off" ? null : at;
      }
      const role = at.getAttribute("role") ?? (at.tagName === "OUTPUT" ? "status" : null);
      if (role === "status" || role === "log" || role === "alert") {
        return at;
      }
    }
    return null;
  };
  /** @type {Record<string, number>} */
  const counts = {};
  /** @param {MutationRecord[]} records */
  const tally = (records) => {
    for (const record of records) {
      const target = record.target;
      const region = regionOf(target instanceof Element ? target : target.parentElement);
      if (region !== null) {
        const name = region.id || region.tagName.toLowerCase();
        counts[name] = (counts[name] ?? 0) + 1;
      }
    }
  };
  const observer = new MutationObserver(tally);
  holder.packLiveWatch?.observer.disconnect();
  holder.packLiveWatch = { observer, counts, tally };
  observer.observe(document.body, { subtree: true, childList: true, characterData: true });
  return [...document.querySelectorAll("[aria-live], [role], output")]
    .filter((element) => regionOf(element) === element)
    .map((element) => element.id || element.tagName.toLowerCase());
};
