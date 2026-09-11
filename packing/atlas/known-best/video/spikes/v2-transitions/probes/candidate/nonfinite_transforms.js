// How many drawn squares carry a transform that is not a finite number.
() =>
  Array.from(document.querySelectorAll("#squares g"))
    .filter((g) => g.style.display !== "none")
    .map((g) => g.getAttribute("transform") || "")
    .filter((t) => /NaN|Infinity/.test(t)).length;
