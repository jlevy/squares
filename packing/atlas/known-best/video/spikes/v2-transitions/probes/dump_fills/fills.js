// Every visible square's identity beside the fill it is painted, as [identity, fill].
() =>
  Array.from(/** @type {NodeListOf<SVGGElement>} */ (document.querySelectorAll("#squares g")))
    .filter((g) => g.style.display !== "none")
    .map((g) => [
      g.dataset.identity,
      /** @type {Element} */ (g.firstElementChild).getAttribute("fill"),
    ]);
