// Every square of the current n and the transform it sits at, at the instant on the clock.
() =>
  Array.from(document.querySelectorAll("#squares g[data-identity]"))
    .filter((g) => Number(g.dataset.identity) <= window.atlasTransitions.state().n)
    .map((g) => [g.dataset.identity, g.getAttribute("transform")]);
