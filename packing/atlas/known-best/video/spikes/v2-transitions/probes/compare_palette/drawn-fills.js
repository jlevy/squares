// What the stage is actually painting, read off the DOM: the fill of every square it draws. The
// page has no accessor that reports the frame's fills, and reading the elements is the only
// answer that cannot disagree with what a viewer sees.
() =>
  Array.from(
    /** @type {NodeListOf<SVGGElement>} */ (document.querySelectorAll("#squares g[data-identity]")),
  )
    .filter((g) => g.style.display !== "none")
    .map((g) => /** @type {Element} */ (g.firstElementChild).getAttribute("fill"));
