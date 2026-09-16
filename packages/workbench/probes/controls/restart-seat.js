// Where restart sits among the controls' buttons, and how it is drawn: beside play, on the
// same row, with a glyph and a name of its own.
() => {
  const bs = Array.from(document.querySelectorAll("#controls button"));
  const i = bs.findIndex((b) => b.id === "restart");
  const j = bs.findIndex((b) => b.id === "play");
  const restart = bs[i];
  const play = bs[j];
  if (restart === undefined || play === undefined) {
    throw new Error("probe requires restart and play controls");
  }
  const r = restart.getBoundingClientRect();
  const q = play.getBoundingClientRect();
  return {
    i,
    j,
    sameRow: Math.abs(r.top - q.top) < 2,
    gap: r.left - q.right,
    glyph: restart.querySelector("svg") !== null,
    name: restart.getAttribute("aria-label"),
  };
};
