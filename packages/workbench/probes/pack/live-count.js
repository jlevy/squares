// Stop the count pack/live-watch began and return its mutations per live region.
() => {
  /** @typedef {{observer: MutationObserver, counts: Record<string, number>, tally: (records: MutationRecord[]) => void}} LiveWatch */
  const holder = /** @type {Window & {packLiveWatch?: LiveWatch}} */ (window);
  const watch = holder.packLiveWatch;
  if (watch === undefined) {
    throw new Error("probe requires pack/live-watch to have run");
  }
  watch.tally(watch.observer.takeRecords());
  watch.observer.disconnect();
  holder.packLiveWatch = undefined;
  return watch.counts;
};
