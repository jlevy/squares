// Which identities are drawn rather than hidden, in order.
() =>
  Array.from(
    /** @type {NodeListOf<SVGGElement>} */ (document.querySelectorAll("#squares g[data-identity]")),
  )
    .filter((g) => g.style.display !== "none")
    .map((g) => Number(g.dataset.identity))
    .sort((a, b) => a - b);
