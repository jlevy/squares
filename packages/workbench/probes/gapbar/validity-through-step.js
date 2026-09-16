// The gap bar through one step, at instants read from the step's own schedule rather than from
// seconds a timing change would move: halfway through the dwell, a quarter, a half and three
// quarters of the move, the move's end, and the last instant. Each row is [t, whether the bar
// calls the frame a packing, the deepest penetration, the hand's drawn opacity, the first failing
// clause, the tolerance applied, and whether the frame was assessed at the catalogue's stored
// precision or as a packing]. The snap and
// the blind run are left as they were found. o.n is the step's n, o.style the style.
/** @param {{n: number, style: import("../../src/api/workbench-api.js").AtlasStyle}} o */
(o) => {
  const api = window.atlasTransitions;
  const hand = document.getElementById("gapbar-hand");
  if (hand == null) {
    throw new Error("probe requires #gapbar-hand");
  }
  api.pause();
  api.setStyle(o.style);
  api.setStepN(o.n);
  const s = api.schedule();
  const move = s.moveEnd - s.moveStart;
  const instants = [
    s.moveStart / 2,
    s.moveStart + move / 4,
    s.moveStart + move / 2,
    s.moveStart + (3 * move) / 4,
    s.moveEnd,
    api.duration(),
  ];
  return instants.map((t) => {
    api.seek(t);
    const bar = api.gapBar();
    return [
      t,
      bar.valid,
      bar.overlap,
      Number(getComputedStyle(hand).opacity),
      bar.reason,
      bar.tolerance,
      bar.precision,
    ];
  });
};
