// The mask's own lines: whether the group is drawn at all, how many lines it carries, and
// how they split between met and unmet.
() => {
  const g = document.getElementById("mask-links");
  if (g == null) {
    throw new Error("probe requires #mask-links");
  }
  const lines = Array.from(g.querySelectorAll("line")).filter((l) => l.style.display !== "none");
  /** @param {string} kind */
  const cls = (kind) => lines.filter((line) => line.getAttribute("class") === kind).length;
  return {
    shown: g.style.display !== "none",
    drawn: lines.length,
    met: cls("met"),
    unmet: cls("unmet"),
  };
};
