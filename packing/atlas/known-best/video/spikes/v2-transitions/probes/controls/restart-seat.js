// Where restart sits among the controls' buttons, and how it is drawn: beside play, on the
// same row, with a glyph and a name of its own.
() => {
  const bs = Array.from(document.querySelectorAll("#controls button"));
  const i = bs.findIndex((b) => b.id === "restart");
  const j = bs.findIndex((b) => b.id === "play");
  const r = bs[i].getBoundingClientRect();
  const q = bs[j].getBoundingClientRect();
  return {
    i,
    j,
    sameRow: Math.abs(r.top - q.top) < 2,
    gap: r.left - q.right,
    glyph: bs[i].querySelector("svg") !== null,
    name: bs[i].getAttribute("aria-label"),
  };
};
