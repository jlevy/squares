// Two angles walked through all five contact counts, side by side, so a shared angle can be
// compared shade for shade. o.angles is the pair.
(o) =>
  [0, 1, 2, 3, 4].map((k) => [
    window.atlasTransitions.fillsFor([o.angles[0]], [k])[0],
    window.atlasTransitions.fillsFor([o.angles[1]], [k])[0],
  ]);
