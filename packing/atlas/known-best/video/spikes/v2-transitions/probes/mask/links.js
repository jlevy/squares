// The mask's own lines: whether the group is drawn at all, how many lines it carries, and
// how they split between met and unmet.
() => {
  const g = document.getElementById("mask-links");
  const lines = Array.from(g.querySelectorAll("line")).filter((l) => l.style.display !== "none");
  const cls = (k) => lines.filter((l) => l.getAttribute("class") === k).length;
  return {
    shown: g.style.display !== "none",
    drawn: lines.length,
    met: cls("met"),
    unmet: cls("unmet"),
  };
};
