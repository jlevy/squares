// How many pool elements, hidden ones included, carry a transform that is not a finite number.
() =>
  Array.from(document.querySelectorAll("#squares g"))
    .map((g) => g.getAttribute("transform") || "")
    .filter((t) => /NaN|Infinity/.test(t)).length;
