// Several pairs of angles, each walked through all five contact counts side by side, so every
// shared angle a checker found can be compared shade for shade in one turn. The answer has one
// entry per pair, each five [fill of the first angle, fill of the second] rows. o.pairs is the
// list of [angle, angle].
/** @param {{pairs: [number, number][]}} o */
(o) =>
  o.pairs.map((pair) =>
    [0, 1, 2, 3, 4].map((k) => [
      window.atlasTransitions.fillsFor([pair[0]], [k])[0],
      window.atlasTransitions.fillsFor([pair[1]], [k])[0],
    ]),
  );
