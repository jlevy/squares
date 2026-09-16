// Two squares of the drawn frame that touch side to side along x, axis-aligned and level: the
// index of the left one and of its neighbour, or null if the frame has none. o.n is the count.
/** @param {{n: number}} o */
(o) => {
  const api = window.atlasTransitions;
  for (let i = 0; i < o.n; i++) {
    for (let j = 0; j < o.n; j++) {
      const a = api.poseOf(i);
      const b = api.poseOf(j);
      if (
        a !== null &&
        b !== null &&
        a[2] % 90 === 0 &&
        b[2] % 90 === 0 &&
        a[1] === b[1] &&
        b[0] - a[0] === 1
      ) {
        return [i, j];
      }
    }
  }
  return null;
};
