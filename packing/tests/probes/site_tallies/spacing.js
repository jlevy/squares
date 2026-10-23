// Tally spacing: each tally set as a line of its own, with its block margins and the
// space to the blocks either side, and each dot between a tally's counts, with whether
// it is the shared separator, its word spacing and the space either side of the dot
// (null where a line ends beside the dot).
() => {
  /** @param {string} value */
  const px = (value) => Number.parseFloat(value) || 0;
  const tallies = ".site-credit-tally, .site-profile-summary";
  const lines = [
    ...document.querySelectorAll(".site-profile-summary, p:has(> .site-profile-tally)"),
  ].map((element) => {
    const style = getComputedStyle(element);
    const rect = element.getBoundingClientRect();
    const before = element.previousElementSibling?.getBoundingClientRect();
    const after = element.nextElementSibling?.getBoundingClientRect();
    return {
      kind: element.matches(".site-profile-summary") ? "summary" : "profile",
      marginTop: px(style.marginTop),
      marginBottom: px(style.marginBottom),
      above: before ? rect.top - before.bottom : null,
      below: after ? after.top - rect.bottom : null,
    };
  });
  /** @type {{shared: boolean, wordSpacing: number, fontSize: number, before: number | null, after: number | null}[]} */
  const dots = [];
  for (const tally of document.querySelectorAll(tallies)) {
    const walker = document.createTreeWalker(tally, NodeFilter.SHOW_TEXT);
    for (let node = walker.nextNode(); node; node = walker.nextNode()) {
      const text = /** @type {Text} */ (node);
      const parent = text.parentElement;
      // A tally inside a tally is measured once, as its own.
      if (!parent || parent.closest(tallies) !== tally) {
        continue;
      }
      /** @param {number} start */
      const box = (start) => {
        const range = document.createRange();
        range.setStart(text, start);
        range.setEnd(text, start + 1);
        return range.getBoundingClientRect();
      };
      for (let at = text.data.indexOf("·"); at >= 0; at = text.data.indexOf("·", at + 1)) {
        const style = getComputedStyle(parent);
        const spaced = at > 0 && text.data[at - 1] === " " && text.data[at + 1] === " ";
        const boxes = spaced ? { lead: box(at - 1), dot: box(at), trail: box(at + 1) } : null;
        const inline =
          boxes !== null && boxes.lead.top === boxes.dot.top && boxes.trail.top === boxes.dot.top;
        dots.push({
          shared: parent.matches(".site-tally-sep"),
          wordSpacing: px(style.wordSpacing),
          fontSize: px(style.fontSize),
          before: inline && boxes ? boxes.dot.left - boxes.lead.left : null,
          after: inline && boxes ? boxes.trail.right - boxes.dot.right : null,
        });
      }
    }
  }
  return {
    lines,
    dots,
    overflow: document.documentElement.scrollWidth > innerWidth,
  };
};
